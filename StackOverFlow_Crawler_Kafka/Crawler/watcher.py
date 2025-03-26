# watcher.py

from .interfaces import WatcherInterface
import time
from pathlib import Path
from .scraper import StackOverflowScraper_Facade as StackOverflowScraper
from .display import QuestionDisplay
from .notification_handler import Notifier as notifier
from .notification_handler import NotificationType as notif_type


class QuestionWatcher_Observer(WatcherInterface):

    def __init__(self, language: str, check_interval: int = 60):
        self.language = language
        self.check_interval = check_interval
        self.scraper = StackOverflowScraper(language=language, max_questions=500)
        self._storage_path = Path(f"last_seen_id_{self.language}.txt")
        self.last_seen_id = self._load_last_seen_id()
        self.new_questions_sorted = None

    def start_watching(self):
        """Initiate monitoring loop"""
        notifier.notify(notif_type.WATCHER_STARTED)
        try:
            while True:
                self.check_new_questions()
                time.sleep(self.check_interval)
        except KeyboardInterrupt:

            notifier.notify(notif_type.WATCHER_STOPPED)

    def check_new_questions(self):
        """Single check cycle implementation"""
        def stop_condition(q): return q.id <= self.last_seen_id
        questions = self.scraper.get_questions(stop_condition=stop_condition)
        new_questions = self._extract_new_crawled_questions(questions)

        if new_questions:
            self._update_and_get_max_id(new_questions)
            notifier.notify(notif_type.NEW_QUESTIONS)
            QuestionDisplay.display(self.new_questions_sorted)
        else:
            notifier.notify(notif_type.NO_NEW_QUESTIONS)

    def _update_and_get_max_id(self, new_questions):
        self.new_questions_sorted = sorted(new_questions, key=lambda q: q.id)
        self.last_seen_id = self.new_questions_sorted[-1].id
        self._save_last_seen_id(self.last_seen_id)

    def _extract_new_crawled_questions(self, questions):
        return [q for q in questions if q.id > self.last_seen_id]

    # State management methods

    def _load_last_seen_id(self) -> int:
        return self._last_crawled_id() if self._previously_crawled() else self._crawl_last_id()

    def _crawl_last_id(self):
        try:
            questions = self.scraper.get_questions()
            return self._get_max_crawled_id(questions)
        except Exception as e:
            print(f"Error initializing last seen ID: {e}")
            return 0

    def _get_max_crawled_ID(self, questions):
        return max(q.id for q in questions) if questions else 0

    def _initialize_last_id(self) -> int:
        try:
            questions = self.scraper.get_questions()
            return self._get_max_id(questions)
        except Exception as e:
            print(f"Error initializing last seen ID: {e}")
            return 0

    def _previously_crawled(self):
        return self._get_storage_path()

    def _save_last_seen_id(self, last_id: int):
        with open(self._get_storage_path(), 'w') as f:
            f.write(str(last_id))

    def _get_storage_path(self):
        return Path(f"last_seen_id_{self.language}.txt")
