# crawler.py

from .scraper import StackOverflowScraperFacade
from .fetcher import FetcherStrategy
from .parser import QuestionParserTemplateMethod
from models import Question


class QuestionCrawler:
    def __init__(self, language: str, max_questions: int = 100):
        self.language = language.lower()
        self.max_questions = max_questions
        self.scraper = self._create_scraper()

    def _create_scraper(self):
        base_url = "https://stackoverflow.com"
        # Dependency injection: Inject fetcher and parser implementations
        fetcher = FetcherStrategy(
            headers={"User-Agent": "Mozilla/5.0"},
            url_builder=lambda p: f"{base_url}/questions/tagged/{self.language}?page={p}",
            retries=3,
            delay=2
        )
        parser = QuestionParserTemplateMethod(base_url=base_url)
        return StackOverflowScraperFacade(fetcher, parser, self.max_questions)

    def crawl(self) -> list[Question]:
        """Fetch questions up to max_questions."""
        return self.scraper.get_questions()
