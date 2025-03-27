from .interfaces import WatcherInterface
import time
from pathlib import Path
import logging
from typing import Optional, List
from .notification_handler import Notifier, NotificationType
from .display import QuestionDisplay
from .scraper import StackOverflowScraper_Facade
from .fetcher import Fetcher_Strategy
from .parser import QuestionParser_Template_Method
from models import Question

logging.basicConfig(level=logging.INFO)


class QuestionWatcher(WatcherInterface):
    def __init__(self, language: str, check_interval: int = 60,
                 scraper=None, notifier=None, display=None,
                 storage_path: Optional[Path] = None):
        self.language = language.lower()
        self.check_interval = check_interval
        self.scraper = scraper or self._create_default_scraper()
        self.notifier = notifier or Notifier()
        self.display = display or QuestionDisplay()
        self.storage_path = storage_path or Path(f"last_seen_id_{self.language}.txt")
        self.last_seen_id = self._load_last_seen_id()

    def _create_default_scraper(self):
        base_url = "https://stackoverflow.com"
        return StackOverflowScraper_Facade(
            fetcher=Fetcher_Strategy(
                headers={"User-Agent": "Mozilla/5.0"},
                url_builder=lambda p: f"{base_url}/questions/tagged/{self.language}?page={p}",
                retries=3,
                delay=2
            ),
            parser=QuestionParser_Template_Method(base_url=base_url),
            max_questions=50
        )

    def _load_last_seen_id(self) -> int:
        try:
            if self.storage_path.exists():
                with open(self.storage_path, 'r') as f:
                    return int(f.read().strip())
            return 0
        except (ValueError, IOError) as e:
            logging.warning(f"Failed to load last ID: {e}")
            return 0

    def start_watching(self):
        self.notifier.notify(NotificationType.WATCHER_STARTED,
                             language=self.language,
                             interval=self.check_interval)
        try:
            while True:
                self.check_new_questions()
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.notifier.notify(NotificationType.WATCHER_STOPPED)

    def check_new_questions(self):
        try:
            questions = self.scraper.get_questions(
                stop_condition=lambda q: q.id <= self.last_seen_id
            )
            new_questions = [q for q in questions if q.id > self.last_seen_id]

            if new_questions:
                new_questions.sort(key=lambda q: q.id)
                self.last_seen_id = new_questions[-1].id
                self._save_last_seen_id(self.last_seen_id)
                self.notifier.notify(NotificationType.NEW_QUESTIONS, count=len(new_questions))
                self.display.display(new_questions)
            else:
                self.notifier.notify(NotificationType.NO_NEW_QUESTIONS)

        except Exception as e:
            logging.error(f"Error checking questions: {e}")

    def _save_last_seen_id(self, last_id: int):
        try:
            with open(self.storage_path, 'w') as f:
                f.write(str(last_id))
        except IOError as e:
            logging.error(f"Failed to save last ID: {e}")
