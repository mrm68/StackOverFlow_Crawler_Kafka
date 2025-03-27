# interfaces.py

from abc import ABC, abstractmethod
from typing import Iterable, Optional, Callable, List
from models import Question


class FetcherInterface(ABC):
    @abstractmethod
    def fetch(self, page: int) -> Optional[str]:
        """Fetch HTML content for a specific page number."""
        pass


class ParserInterface(ABC):
    @abstractmethod
    def parse(self, html: str) -> List[Question]:
        """Convert HTML to structured Question objects."""
        pass


class ScraperInterface(ABC):
    @abstractmethod
    def get_questions(self, stop_condition: Optional[Callable[[Question], bool]]) -> List[Question]:
        """Retrieve questions with optional filtering."""
        pass


class StreamInterface(ABC):
    @abstractmethod
    def stream(self, stop_condition: Optional[Callable[[Question], bool]]) -> Iterable[Question]:
        """Generate questions through lazy evaluation."""
        pass


class WatcherInterface(ABC):
    @abstractmethod
    def start_watching(self) -> None:
        """Initiates the monitoring loop for new questions."""
        pass

    @abstractmethod
    def check_new_questions(self) -> None:
        """Executes a single check cycle."""
        pass


class DisplayInterface(ABC):
    @staticmethod
    @abstractmethod
    def display(questions: List[Question]):
        """Present questions in readable format."""
        pass
