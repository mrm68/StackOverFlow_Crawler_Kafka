# display.py

from typing import List
from models import Question


class QuestionDisplay:
    """Handler for displaying questions"""

    @staticmethod
    def display(questions: List[Question]):
        """Display questions in a formatted way"""
        for idx, question in enumerate(questions, 1):
            print(f"{idx}. [{question.id}] {question.title}")
            print(f"   📅 {question.timestamp}")
            print(f"   🔗 {question.link}")
            print(f"   📝 {question.excerpt}")
            print(f"   🏷️ {', '.join(question.tags)}")
            print("-" * 80)
