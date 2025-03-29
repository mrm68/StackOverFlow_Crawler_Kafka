# scraper.py

from .interfaces import ScraperInterface, FetcherInterface, ParserInterface
from models import Question
from typing import List, Optional, Callable
import logging
from .notification_handler import NotificationType, Notifier
from .tracedecorator import log_usage

logger = logging.getLogger(__name__)


class StackOverflowScraperFacade(ScraperInterface):
    @log_usage()
    def __init__(self, fetcher: FetcherInterface,
                 parser: ParserInterface, max_questions: int,
                 notifier: Notifier):
        self.fetcher = fetcher
        self.parser = parser
        self.max_questions = max_questions
        self.notifier = self._generate_notifier(notifier)

    @log_usage()
    def _generate_notifier(self, notifier):
        return Notifier() if not notifier else Notifier()

    @log_usage()
    def scrape(self, max_questions: int = None,
               stop_condition: Optional[Callable[[Question], bool]] = None) -> List[Question]:
        questions = []
        page = 1
        limit = self._read_max_questions_limit(max_questions)

        while len(questions) < limit:
            html = self.fetcher.fetch(page)

            if not html:
                self.notifier.notify(NotificationType.NO_HTML_PARSED)
                break

            page_questions = self.parser.parse(html)
            if not page_questions:
                self.notifier.notify(NotificationType.NO_QUESTIONS_PARSED)
                break

            if stop_condition:
                page_questions = [q for q in page_questions if not stop_condition(q)]
                if not page_questions:
                    break

            questions.extend(page_questions)
            page += 1

        return questions[:limit]

    @log_usage()
    def _read_max_questions_limit(self, max_questions):
        return max_questions if max_questions is not None else self.max_questions

    @log_usage()
    def get_questions(self) -> List[Question]:
        return self.scrape()
