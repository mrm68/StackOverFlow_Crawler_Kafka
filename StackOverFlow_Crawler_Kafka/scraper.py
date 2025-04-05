import requests
from typing import Callable, Optional, List
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from models import Question
import time


class StackOverflowScraper:
    """Scraper for StackOverflow questions with pagination support"""
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
        """Build the search URL for the given language and page number"""
        return f"{self.BASE_URL}/questions/tagged/{self.language}?" \
            f"sort=newest&pageSize=50&page={page}"

    def fetch_page(self, page: int) -> Optional[str]:
        """Fetch the HTML content of the questions page"""
        for _ in range(3):  # Retry up to 3 times
            try:
                response = requests.get(
                    self.build_url(page), headers=self.headers)
                response.raise_for_status()
                return response.text
            except RequestException as e:
                print(f"Error fetching page {page}: {e}")
                time.sleep(2)  # Wait before retry
        return None

    def parse_page(self, html: str) -> List[Question]:
        """Parse the HTML content and extract questions"""
        soup = BeautifulSoup(html, "html.parser")
        questions = []

        for question in soup.select(".s-post-summary"):
            link = self._extract_link(question)
            try:
                questions.append(Question(
                    id=self._extract_id(link),
                    title=self._extract_title(question),
                    link=link,
                    excerpt=self._extract_excerpt(question),
                    tags=self._extract_tags(question),
                    timestamp=self._extract_timestamp(question)
                ))
            except Exception as e:
                print(f"Error parsing question: {e}")
                continue

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
        """Extract question ID from link"""
        try:
            parts = [p for p in link.split('/') if p.isdigit()]
            return int(parts[-1]) if parts else 0
        except (IndexError, ValueError):
            return 0

    def get_questions(
            self,
            stop_condition: Optional[Callable[[Question], bool]] = None
    ) -> List[Question]:
        """Get questions with optional stop condition"""
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
