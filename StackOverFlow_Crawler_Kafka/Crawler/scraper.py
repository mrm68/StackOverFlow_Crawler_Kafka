# scraper.py

from .interfaces import ScraperInterface, FetcherInterface, ParserInterface
from models import Question
from typing import List, Optional, Callable
import logging

logger = logging.getLogger(__name__)


class StackOverflowScraperFacade(ScraperInterface):
    def __init__(self, fetcher: FetcherInterface, parser: ParserInterface, max_questions: int):
        self.fetcher = fetcher
        self.parser = parser
        self.max_questions = max_questions

    def scrape(self, max_questions: int = None,
               stop_condition: Optional[Callable[[Question], bool]] = None) -> List[Question]:
        questions = []
        page = 1
        limit = max_questions if max_questions is not None else self.max_questions

        while len(questions) < limit:
            try:
                html = self.fetcher.fetch(page)
            except Exception as e:
                logger.error(f"Fetching page {page} failed: {e}")
                break

            if not html:
                logger.info("No HTML returned, ending scrape.")
                break

            page_questions = self.parser.parse(html)
            if not page_questions:
                logger.info("No questions parsed, ending scrape.")
                break

            if stop_condition:
                page_questions = [q for q in page_questions if not stop_condition(q)]
                if not page_questions:
                    break

            questions.extend(page_questions)
            page += 1

        return questions[:limit]

    def get_questions(self) -> List[Question]:
        return self.scrape()
