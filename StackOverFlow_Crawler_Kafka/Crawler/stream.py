# stream.py

from .interfaces import StreamInterface
from itertools import islice, takewhile, count
from typing import Callable, Iterable, Optional
from models import Question


class QuestionStream_Iterator(StreamInterface):
    """
    Iterator Pattern Implementation

    Responsibilities:
    - Provide lazy question loading
    - Handle pagination transparently
    - Support early termination

    Implements: StreamInterface
    """

    def __init__(self, fetcher, parser, max_questions=50):
        self.fetcher = fetcher
        self.parser = parser
        self.max_questions = max_questions

    def stream(
        self, stop_condition: Optional[Callable[[Question], bool]] = None
    ) -> Iterable[Question]:
        """Main streaming entry point"""
        try:
            # Generate pages lazily using the fetcher
            page_generator = (self.fetcher.fetch(p) for p in count(1))
            # Parse each page and yield questions
            parsed_questions = (
                q for page in page_generator if page for q in self.parser.parse(page)
            )

            # Apply the optional stop condition
            if stop_condition:
                parsed_questions = takewhile(
                    lambda q: not stop_condition(q), parsed_questions
                )

            # Limit the number of questions to the max_questions
            return islice(parsed_questions, self.max_questions)
        except Exception as e:
            raise RuntimeError(f"Error while streaming questions: {e}")
