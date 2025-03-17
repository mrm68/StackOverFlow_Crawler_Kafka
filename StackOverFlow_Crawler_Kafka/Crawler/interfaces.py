# interfaces.py

from abc import ABC, abstractmethod
from typing import Iterable, Optional, Callable, List
from models import Question

"""
Gherkin Interface Definitions

Feature: Fetcher Interface
  Scenario: Fetch page content
    Given a page number
    When fetching content
    Then return HTML text or None on failure
"""


class FetcherInterface(ABC):
    @abstractmethod
    def fetch(self, page: int) -> Optional[str]:
        """Fetch HTML content for a specific page number"""
        pass


"""
Feature: Parser Interface
  Scenario: Parse HTML content
    Given valid HTML content
    When parsing questions
    Then return list of Question objects
"""


class ParserInterface(ABC):
    @abstractmethod
    def parse(self, html: str) -> List[Question]:
        """Convert HTML to structured Question objects"""
        pass


"""
Feature: Scraper Interface
  Scenario: Scrape questions
    Given scraping parameters
    When collecting questions
    Then return questions matching criteria
"""


class ScraperInterface(ABC):
    @abstractmethod
    def get_questions(self, stop_condition: Optional[Callable[[Question], bool]]) -> List[Question]:
        """Retrieve questions with optional filtering"""
        pass


"""
Feature: Stream Interface
  Scenario: Stream questions
    Given pagination parameters
    When streaming questions
    Then yield questions until limit reached
"""


class StreamInterface(ABC):
    @abstractmethod
    def stream(self, stop_condition: Optional[Callable[[Question], bool]]) -> Iterable[Question]:
        """Generate questions through lazy evaluation"""
        pass


"""
Feature: Watcher Interface
  Scenario: Monitor questions
    Given monitoring parameters
    When watching for new questions
    Then detect and notify about new entries
"""


class WatcherInterface(ABC):
    @abstractmethod
    def start_watching(self):
        """Initiate continuous monitoring process"""
        pass

    @abstractmethod
    def check_new_questions(self):
        """Perform single check cycle for new questions"""
        pass


"""
Feature: Display Interface
  Scenario: Render questions
    Given list of questions
    When displaying results
    Then format output for human consumption
"""


class DisplayInterface(ABC):
    @staticmethod
    @abstractmethod
    def display(questions: List[Question]):
        """Present questions in readable format"""
        pass
