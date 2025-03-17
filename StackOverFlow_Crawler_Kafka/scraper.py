# scraper.py
from typing import Callable, Optional, List
import requests
from typing import Callable, Optional, Iterable
from requests.exceptions import RequestException
from bs4 import BeautifulSoup, Tag
from models import Question
import time
from functools import partial
from itertools import islice, takewhile, count


# Strategy Pattern: Encapsulates different fetching strategies
class Fetcher:
    """Strategy pattern for fetching pages."""

    def __init__(self, headers, url_builder):
        self.headers = headers
        self.url_builder = url_builder

    def fetch(self, page: int) -> Optional[str]:
        for _ in range(3):
            try:
                response = requests.get(
                    self.url_builder(page), headers=self.headers
                )
                response.raise_for_status()
                return response.text
            except RequestException as e:
                print(f"Error fetching page {page}: {e}")
                time.sleep(2)
        return None


# Null Object Pattern: Handles missing elements gracefully
class ElementExtractor:
    """Null object pattern for element extraction."""

    def __init__(self, selector, attribute=None, default=""):
        self.selector = selector
        self.attribute = attribute
        self.default = default

    def extract(self, element: Tag) -> str:
        result = element.select_one(self.selector)
        return self._get_value(result) if result else self.default

    def _get_value(self, element):
        return element[self.attribute] if self.attribute else element.text.strip()


# Template Method Pattern: Standardizes the parsing process
class QuestionParser:
    """Template method pattern for parsing questions."""

    def __init__(self, base_url):
        self.base_url = base_url
        self.extractors = {
            'title': ElementExtractor(".s-post-summary--content-title a"),
            'link': ElementExtractor(
                ".s-post-summary--content-title a", "href"
            ),
            'excerpt': ElementExtractor(".s-post-summary--content-excerpt"),
            'timestamp': ElementExtractor(
                ".s-user-card--time .relativetime", "title", "Unknown time"
            ),
        }

    def parse(self, html: str) -> Iterable[Question]:
        soup = BeautifulSoup(html, "html.parser")
        return map(self._parse_question, soup.select(".s-post-summary"))

    def _parse_question(self, question_element: Tag) -> Question:
        link = self._build_link(
            self.extractors['link'].extract(question_element)
        )
        return Question(
            id=self._extract_id(link),
            title=self.extractors['title'].extract(question_element),
            link=link,
            excerpt=self.extractors['excerpt'].extract(question_element),
            tags=[t.text for t in question_element.select(".post-tag")],
            timestamp=self.extractors['timestamp'].extract(question_element)
        )

    def _build_link(self, path: str) -> str:
        return f"{self.base_url}{path}" if path else ""

    def _extract_id(self, link: str) -> int:
        parts = (p for p in link.split('/') if p.isdigit())
        return int(next(parts, 0))

# Iterator Pattern: Provides lazy evaluation of questions


class QuestionStream:
    """Iterator pattern for question pagination."""

    def __init__(self, fetcher, parser, max_questions=50):
        self.fetcher = fetcher
        self.parser = parser
        self.max_questions = max_questions

    def stream(
        self, stop_condition: Optional[Callable[[Question], bool]] = None
    ) -> Iterable[Question]:
        page_generator = (self.fetcher.fetch(p) for p in count(1))
        parsed_questions = (
            q for page in page_generator if page for q in self.parser.parse(page)
        )

        if stop_condition:
            parsed_questions = takewhile(
                lambda q: not stop_condition(q), parsed_questions
            )

        return islice(parsed_questions, self.max_questions)


# Facade Pattern: Simplifies the interface for scraping operations


class StackOverflowScraper:
    """Scraper for StackOverflow questions with pagination support."""
    BASE_URL = "https://stackoverflow.com"
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    }

    def __init__(self, language: str, max_questions: int = 50,
                 user_agent: Optional[str] = None):
        self.language = language
        self.max_questions = max_questions
        self.headers = {
            "User-Agent": user_agent} if user_agent else self.DEFAULT_HEADERS

    def build_url(self, page: int = 1) -> str:
        """Build the search URL for the given language and page number."""
        return (
            f"{self.BASE_URL}/questions/tagged/{self.language}"
            f"?sort=newest&pageSize=50&page={page}"
        )

    def fetch_page(self, page: int) -> Optional[str]:
        """Fetch the HTML content of the questions page."""
        for _ in range(3):  # Retry up to 3 times
            try:
                response = requests.get(
                    self.build_url(page), headers=self.headers
                )
                response.raise_for_status()
                return response.text
            except RequestException as e:
                print(f"Error fetching page {page}: {e}")
                time.sleep(2)  # Wait before retry
        return None

    def parse_page(self, html: str) -> List[Question]:
        """Parse the HTML content and extract questions."""
        soup = BeautifulSoup(html, "html.parser")
        questions = []

        for question in soup.select(".s-post-summary"):
            link = self._extract_link(question)
            question_data = {
                "id": self._extract_id(link),
                "title": self._extract_title(question),
                "link": link,
                "excerpt": self._extract_excerpt(question),
                "tags": self._extract_tags(question),
                "timestamp": self._extract_timestamp(question)
            }
            # Create a Pydantic Question object
            questions.append(Question(**question_data))

        return questions

    def _extract_title(self, question_element) -> str:
        element = question_element.select_one(
            ".s-post-summary--content-title a")
        return element.text.strip() if element else "No title"

    def _extract_link(self, question_element) -> str:
        element = question_element.select_one(
            ".s-post-summary--content-title a")
        return f"{self.BASE_URL}{element['href']}" if element else ""

    def _extract_excerpt(self, question_element) -> str:
        element = question_element.select_one(
            ".s-post-summary--content-excerpt")
        return element.text.strip() if element else "No excerpt"

    def _extract_tags(self, question_element) -> List[str]:
        return [tag.text for tag in question_element.select(".post-tag")]

    def _extract_timestamp(self, question_element) -> str:
        element = question_element.select_one(
            ".s-user-card--time .relativetime")
        if element and element.has_attr("title"):
            return element["title"]
        else:
            return "Unknown time"

    def _extract_id(self, link: str) -> int:
        """Extract question ID from link."""
        try:
            parts = [p for p in link.split('/') if p.isdigit()]
            return int(parts[-1]) if parts else 0
        except (IndexError, ValueError):
            return 0

    def get_questions(
            self,
            stop_condition: Optional[Callable[[Question], bool]] = None
    ) -> List[Question]:
        """Get questions with optional stop condition."""
        questions = []
        page = 1

        while len(questions) < self.max_questions:
            html = self.fetch_page(page)
            if not html:
                break

            new_questions = self.parse_page(html)
            if not new_questions:
                break

            if stop_condition:
                filtered_questions = []
                for q in new_questions:
                    if stop_condition(q):
                        break
                    filtered_questions.append(q)
                questions.extend(filtered_questions)
                if len(filtered_questions) < len(new_questions):
                    break
            else:
                questions.extend(new_questions)

            page += 1
            # Add safety limit
            if page > 100:  # Prevent infinite loop
                break

        return questions[:self.max_questions]
