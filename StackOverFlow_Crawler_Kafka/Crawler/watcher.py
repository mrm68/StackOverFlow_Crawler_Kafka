# watcher.py

from .interfaces import WatcherInterface
import time
from pathlib import Path
import logging
from .notification_handler import Notifier, NotificationType
from .display import QuestionDisplay
from .scraper import StackOverflowScraper_Facade
from .fetcher import Fetcher_Strategy
from .parser import QuestionParser_Template_Method

logging.basicConfig(level=logging.INFO)


class QuestionWatcher(WatcherInterface):
    def __init__(self, language: str, check_interval: int = 60,
                 scraper=None, notifier=None, display=None,
                 storage_path: Path = None):
        self.language = language  # Initialize language first
        self.check_interval = check_interval

        # Configure default scraper dependencies
        base_url = "https://stackoverflow.com"

        self.scraper = scraper or StackOverflowScraper_Facade(
            fetcher=Fetcher_Strategy(
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                },
                url_builder=lambda page: (
                    f"{base_url}/questions/tagged/{self.language}"  # Use self.language
                    f"?tab=newest&page={page}"
                ),
                retries=3,
                delay=2
            ),
            parser=QuestionParser_Template_Method(base_url=base_url),
            max_questions=50
        )
        self.notifier = notifier or Notifier()
        self.display = display or QuestionDisplay()
        self.storage_path = storage_path or Path(f"last_seen_id_{self.language}.txt")
        self.last_seen_id = self._initialize_last_seen_id()

    def start_watching(self):
        """Initiate monitoring loop with notifications and graceful shutdown."""
        self.notifier.notify(NotificationType.WATCHER_STARTED,
                             language=self.language, interval=self.check_interval)
        try:
            while True:
                self.check_new_questions()
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.notifier.notify(NotificationType.WATCHER_STOPPED)

    def check_new_questions(self):
        """Fetch and handle new questions in a single cycle."""
        try:
            # Fetch questions with a stop condition based on the last seen ID
            questions = self.scraper.get_questions(
                stop_condition=lambda q: q.id <= self.last_seen_id
            )
            new_questions = [q for q in questions if q.id > self.last_seen_id]

            if not new_questions:
                self.notifier.notify(NotificationType.NO_NEW_QUESTIONS)
                return

            # Sort questions by ID, update state, notify, and display them
            self._process_new_questions(new_questions)

        except Exception as e:
            logging.error(f"Error during check cycle: {e}")

    def _initialize_last_seen_id(self) -> int:
        """Initialize the last seen ID from storage or via a fresh scrape."""
        if not self.storage_path.exists():
            return 0

        try:
            with open(self.storage_path, 'r') as f:
                return int(f.read().strip())
        except (ValueError, IOError) as e:
            logging.warning(f"Failed to read last seen ID, defaulting to 0: {e}")
            return 0

    def _process_new_questions(self, new_questions):
        """Sort, update state, save to storage, notify, and display."""
        sorted_questions = sorted(new_questions, key=lambda q: q.id)
        self.last_seen_id = sorted_questions[-1].id
        self._save_last_seen_id(self.last_seen_id)
        self.notifier.notify(NotificationType.NEW_QUESTIONS, count=len(sorted_questions))
        self.display.display(sorted_questions)

    def _save_last_seen_id(self, last_id: int):
        """Persist the last seen ID."""
        try:
            with open(self.storage_path, 'w') as f:
                f.write(str(last_id))
        except IOError as e:
            logging.error(f"Error saving last seen ID: {e}")
