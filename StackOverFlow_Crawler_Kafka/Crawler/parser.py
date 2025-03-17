# parser.py

from typing import List
from .interfaces import ParserInterface
from bs4 import BeautifulSoup, Tag
from models import Question


class QuestionParser_Template_Method(ParserInterface):
    """
    Template Method Pattern Implementation

    Responsibilities:
    - Define parsing algorithm skeleton
    - Handle element extraction details
    - Convert raw HTML to domain objects

    Implements: ParserInterface
    """

    def __init__(self, base_url):
        self.base_url = base_url

    def parse(self, html: str) -> List[Question]:
        """Main parsing entry point"""
        soup = BeautifulSoup(html, "html.parser")
        return [self._parse_question(q) for q in soup.select(".s-post-summary")]

    def _parse_question(self, question_element: Tag) -> Question:
        """Template method implementation"""
        link = self._build_link(
            question_element.select_one(".s-post-summary--content-title a")["href"]
        )
        votes = self._extract_votes(question_element)
        answers = self._extract_answers(question_element)
        views = self._extract_views(question_element)

        return Question(
            id=self._extract_id(link),
            title=self._extract_title(question_element),
            link=link,
            excerpt=self._extract_excerpt(question_element),
            tags=self._extract_tags(question_element),
            timestamp=self._extract_timestamp(question_element),
            votes=votes,
            answers=answers,
            views=views,
        )

    def _extract_votes(self, question_element: Tag) -> int:
        """Extract the number of votes from the question element."""
        votes_element = question_element.select_one(
            ".s-post-summary--stats-item:nth-child(1) .s-post-summary--stats-item-number")
        return int(votes_element.text.strip()) if votes_element else 0

    def _extract_answers(self, question_element: Tag) -> int:
        """Extract the number of answers from the question element."""
        answers_element = question_element.select_one(
            ".s-post-summary--stats-item:nth-child(2) .s-post-summary--stats-item-number")
        return int(answers_element.text.strip()) if answers_element else 0

    def _extract_views(self, question_element: Tag) -> int:
        """Extract the number of views from the question element."""
        views_element = question_element.select_one(
            ".s-post-summary--stats-item:nth-child(3) .s-post-summary--stats-item-number")
        return int(views_element.text.strip()) if views_element else 0

    # Helper methods with clear single responsibilities

    def _build_link(self, path: str) -> str:
        return f"{self.base_url}{path}" if path else ""

    def _extract_id(self, link: str) -> int:
        parts = (p for p in link.split('/') if p.isdigit())
        return int(next(parts, 0))

    def _extract_title(self, element: Tag) -> str:
        return element.text.strip() if element else "No title"

    def _extract_excerpt(self, element: Tag) -> str:
        return element.text.strip() if element else "No excerpt"

    def _extract_tags(self, element: Tag) -> list[str]:
        return [tag.text for tag in element.select(".post-tag")]

    def _extract_timestamp(self, element: Tag) -> str:
        return element["title"] if element and element.has_attr("title") else "Unknown time"
