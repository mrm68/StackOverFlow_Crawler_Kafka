# display.py

from .interfaces import DisplayInterface
from typing import List
from models import Question


class QuestionDisplay(DisplayInterface):
    """
    Presentation Layer Implementation

    Responsibilities:
    - Format question data for CLI output
    - Handle display logic consistently
    - Decouple presentation from business logic

    Implements: DisplayInterface
    """

    @staticmethod
    def _clean_excerpt(excerpt: str) -> str:
        """Clean up the excerpt by removing extra newlines and spaces."""
        # Remove leading/trailing whitespace and collapse multiple spaces/newlines
        return " ".join(excerpt.strip().split())

    @staticmethod
    def display(questions: List[Question]):
        """Render questions in standardized format"""
        for idx, question in enumerate(questions, 1):
            print(f"{idx}. [{question.id}] {question.title}")
            print(f"   📅 {question.timestamp}")
            print(f"   🔗 {question.link}")
            print(f"   📝 {QuestionDisplay._clean_excerpt(question.excerpt)}")
            print(f"   🏷️ {', '.join(question.tags)}")
            print(
                f"   👍 Votes: {question.votes} |"
                f" 📄 Answers: {question.answers} | 👀 Views: {question.views}")
            print("-" * 80)
