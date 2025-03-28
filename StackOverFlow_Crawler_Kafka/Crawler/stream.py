# stream.py

from .interfaces import StreamInterface
from itertools import islice, takewhile, count
from typing import Callable, Iterable, Optional
from models import Question
import logging

logger = logging.getLogger(__name__)


class QuestionStreamIterator(StreamInterface):
    """
    Iterator Pattern Implementation for lazy question loading.
    """

    def __init__(self, fetcher, parser, max_questions=50):
        self.fetcher = fetcher
        self.parser = parser
        self.max_questions = max_questions

    def stream(self,
               stop_condition: Optional[Callable[[Question], bool]] = None) -> Iterable[Question]:
        try:
            page_generator = (self.fetcher.fetch(p) for p in count(1))
            # Parse each page and yield questions.
            parsed_questions = (
                q for page in page_generator if page for q in self.parser.parse(page))
            # Apply the optional stop condition.
            if stop_condition:
                parsed_questions = takewhile(lambda q: not stop_condition(q), parsed_questions)
            # Limit the number of questions to max_questions.
            return islice(parsed_questions, self.max_questions)
        except Exception as e:
            logger.error(f"Error while streaming questions: {e}")
            raise RuntimeError(f"Error while streaming questions: {e}")
