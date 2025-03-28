# display.py

from .interfaces import DisplayInterface
from models import Question
from typing import List


class QuestionDisplay(DisplayInterface):
    @staticmethod
    def display(questions: List[Question]) -> None:
        # Display questions as defined; no changes to the presentation format.
        for idx, question in enumerate(questions, 1):
            print(f"{idx}. [{question.id}] {question.title}")
            print(f"   📅 {question.timestamp}")
            print(f"   🔗 {question.link}")
            print(f"   📝 {question.excerpt}")
            print(f"   🏷️ {', '.join(question.tags)}")
            print(
                f"   👍 Votes: {question.votes} |"
                f" 📄 Answers: {question.answers} |"
                f" 👀 Views: {question.views}")

            print("-" * 80)
