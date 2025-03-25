# scraper.py

from .interfaces import ScraperInterface
from .fetcher import Fetcher_Strategy as Fetcher
from .parser import QuestionParser_Template_Method as QuestionParser
from models import Question
from typing import Callable, Optional, List


class StackOverflowScraper_Facade(ScraperInterface):
    """
    Facade Pattern Implementation

    Responsibilities:
    - Simplify complex scraping operations
    - Coordinate fetcher and parser components
    - Handle pagination and filtering

    Implements: ScraperInterface
    """
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
        self.fetcher = Fetcher(self.headers, self.build_url)
        self.parser = QuestionParser(self.BASE_URL)

    def get_questions(
            self, stop_condition: Optional[Callable[[Question], bool]] = None
    ) -> List[Question]:
        """Facade method: Orchestrate full scraping workflow"""
        questions = []
        page = 1

        while len(questions) < self.max_questions:
            html = self.fetcher.fetch(page)
            if not html:
                break

            new_questions = self.parser.parse(html)
            if not new_questions:
                break

            if stop_condition:
                filtered_questions = [
                    q for q in new_questions if not stop_condition(q)
                ]
                questions.extend(filtered_questions)
                if len(filtered_questions) < len(new_questions):
                    break
            else:
                questions.extend(new_questions)

            page += 1
            if page > 100:  # Safety net
                break

        return questions[:self.max_questions]

    def build_url(self, page: int = 1) -> str:
        """URL construction strategy"""
        return (
            f"{self.BASE_URL}/questions/tagged/{self.language}"
            f"?sort=newest&pageSize=50&page={page}"
        )
