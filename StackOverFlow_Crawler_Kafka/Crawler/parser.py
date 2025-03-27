# parser.py

from typing import List
from .interfaces import ParserInterface
from bs4 import BeautifulSoup, Tag
from models import Question


class QuestionParser_Template_Method(ParserInterface):
    def __init__(self, base_url):
        self.base_url = base_url

    def parse(self, html: str) -> List[Question]:
        """Convert HTML into a list of Question objects."""
        soup = BeautifulSoup(html, "html.parser")
        return [self._parse_question(q) for q in soup.select(".s-post-summary")]

    def _parse_question(self, question_element: Tag) -> Question:
        """Extract question details."""
        link = self._build_link(
            question_element.select_one(".s-post-summary--content-title a")["href"]
        )
        return Question(
            id=self._extract_id(link),
            title=self._extract_text(question_element, ".s-post-summary--content-title a"),
            link=link,
            excerpt=self._extract_text(question_element, ".s-post-summary--content-excerpt"),
            tags=self._extract_tags(question_element),
            timestamp=self._extract_attribute(question_element, "title", ".relativetime"),
            votes=self._extract_stat(question_element, 1),
            answers=self._extract_stat(question_element, 2),
            views=self._extract_stat(question_element, 3),
        )

    def _extract_stat(self, question_element: Tag, nth_child: int) -> int:
        stat_element = question_element.select_one(
            f".s-post-summary--stats-item:nth-child({nth_child}) .s-post-summary--stats-item-number"
        )
        return int(stat_element.text.strip()) if stat_element else 0

    def _extract_tags(self, element: Tag) -> List[str]:
        return [tag.text.strip() for tag in element.select(".post-tag")]

    def _build_link(self, path: str) -> str:
        return f"{self.base_url}{path}" if path else ""

    def _extract_id(self, link: str) -> int:
        parts = (p for p in link.split('/') if p.isdigit())
        return int(next(parts, 0))

    def _extract_text(self, element: Tag, selector: str) -> str:
        sub_element = element.select_one(selector)
        return sub_element.text.strip() if sub_element else "N/A"

    def _extract_attribute(self, element: Tag, attr: str, selector: str) -> str:
        sub_element = element.select_one(selector)
        return sub_element[attr] if sub_element and attr in sub_element.attrs else "N/A"
