# stream.py

from .interfaces import StreamInterface
from itertools import islice, count
from typing import Callable, Iterable, Optional
from models import Question
import logging
from .notification_handler import NotificationType, Notifier
from .tracedecorator import log_usage
logger = logging.getLogger(__name__)


class QuestionStreamIterator(StreamInterface):
    @log_usage()
    def __init__(self, fetcher, parser, max_questions=50, notifier: Notifier = Notifier):
        self.fetcher = fetcher
        self.parser = parser
        self.max_questions = max_questions
        self.notifier = notifier or Notifier()

    @log_usage()
    def stream(
        self,
        stop_condition: Optional[Callable[[Question], bool]] = None
    ) -> Iterable[Question]:
        try:
            page_generator = self._get_page_content_generator()
            parsed_questions = self._parse_questions(page_generator, stop_condition)
            return islice(parsed_questions, self.max_questions)
        except Exception as e:
            self.notifier.notify(NotificationType.STREAMING_ERROR, str(e))

    @log_usage()
    def _parse_questions(self, page_generator, stop_condition=None):
        return (
            q
            for page in page_generator
            if page
            for q in self.parser.parse(page)
            if stop_condition is None or not stop_condition(q)
        )

    @log_usage()
    def _get_page_content_generator(self):
        return (self.fetcher.fetch(p) for p in count(1))
