# interfaces.py

from abc import ABC, abstractmethod
from typing import List, Optional, Callable
from models import Question


class FetcherInterface(ABC):
    @abstractmethod
    def fetch(self, page: int) -> Optional[str]:
        """
        Fetch HTML content for the given page number.
        Returns None if the fetch fails.
        """
        pass


class ParserInterface(ABC):
    @abstractmethod
    def parse(self, html: str) -> List[Question]:
        """
        Parse the provided HTML string and return a list of Question objects.
        """
        pass


class ScraperInterface(ABC):
    @abstractmethod
    def scrape(self, max_questions: int,
               stop_condition: Optional[Callable[[Question], bool]] = None) -> List[Question]:
        """
        Scrape the website and return a list of Question objects up to max_questions.
        If a stop_condition is provided, stop scraping when the condition is met.
        """
        pass


class WatcherInterface(ABC):
    @abstractmethod
    def watch(self, questions: List[Question]) -> List[Question]:
        """
        Compare the provided questions with internal state and return only those that are new.
        """
        pass

    @abstractmethod
    def persist_state(self) -> None:
        """
        Persist the current state (e.g., last seen question id) to storage.
        """
        pass

    @abstractmethod
    def run(self, scraper: ScraperInterface,
            display: 'DisplayInterface', notifier, interval: int) -> None:
        """
        Continuously poll the scraper for new questions, display them, and notify accordingly.
        """
        pass


class DisplayInterface(ABC):
    @abstractmethod
    def display(self, questions: List[Question]) -> None:
        """
        Display the provided list of questions in a human-readable format.
        """
        pass


class StreamInterface(ABC):
    @abstractmethod
    def stream(self, stop_condition: Optional[Callable[[Question], bool]] = None):
        """
        Return an iterator (stream) of questions.
        """
        pass
