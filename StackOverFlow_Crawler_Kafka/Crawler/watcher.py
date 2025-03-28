# watcher.py

from .interfaces import WatcherInterface
from pathlib import Path
import logging
from typing import List
from models import Question
import time
from .notification_handler import NotificationType

logger = logging.getLogger(__name__)


class QuestionWatcher(WatcherInterface):
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.last_id = self._load_state()

    def _load_state(self) -> int:
        try:
            if self.storage_path.exists():
                return int(self.storage_path.read_text())
            return 0
        except (ValueError, IOError) as e:
            logger.warning(f"State load failed: {e}")
            return 0

    def watch(self, questions: List[Question]) -> List[Question]:
        new_questions = self._get_new_questions(questions)
        self.last_id = self._get_max_question_id(new_questions) if new_questions else 0
        return new_questions

    def _get_max_question_id(self, new_questions):
        return max(q.id for q in new_questions)

    def _get_new_questions(self, questions):
        return [q for q in questions if q.id > self.last_id]

    def persist_state(self) -> None:
        try:
            self.storage_path.write_text(str(self.last_id))
        except IOError as e:
            logger.error(f"Failed to persist state: {e}")
            raise

    def run(self, scraper, display, notifier, interval: int = 60) -> None:
        notifier.notify(NotificationType.CRAWLER_STARTED)
        questions = scraper.scrape(max_questions=50)
        try:
            self._start_watching(display, notifier, interval, questions)
        except KeyboardInterrupt:
            notifier.notify(NotificationType.WATCHER_STOPPED)
            self.persist_state()
        except Exception as e:
            notifier.notify(NotificationType.WATCHER_STOPPED)
            logger.error(f"Watcher encountered an error: {e}")
            raise

    def _start_watching(self, display, notifier, interval, questions):
        while True:
            new_questions = self.watch(questions)
            if new_questions:
                notifier.notify(NotificationType.NEW_QUESTIONS, count=len(new_questions))
                display.display(sorted(new_questions, key=lambda q: q.id))
                self.persist_state()
            else:
                notifier.notify(NotificationType.NO_NEW_QUESTIONS)
            time.sleep(interval)
