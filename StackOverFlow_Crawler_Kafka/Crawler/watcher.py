# watcher.py

from .interfaces import WatcherInterface
from pathlib import Path
from typing import List
from models import Question
from .notification_handler import NotificationType, Notifier
from .tracedecorator import log_usage
import asyncio  # Added for async support


class QuestionWatcher(WatcherInterface):
    @log_usage()
    def __init__(self, storage_path: Path, notifier: Notifier):
        self.storage_path = storage_path
        self.last_id = self._load_state()
        self.notifier = notifier or Notifier()

    @log_usage()
    def _load_state(self) -> int:
        try:
            return int(self.storage_path.read_text()) if self.storage_path.exists() else 0
        except (ValueError, IOError) as e:
            self.notifier.notify(NotificationType.STATE_LOADING_FAILURE, e)
            return 0

    @log_usage()
    def watch(self, questions: List[Question]) -> List[Question]:
        new_questions = self._get_new_questions(questions)
        if new_questions:
            self.last_id = self._get_max_question_id(new_questions)
        return new_questions

    @log_usage()
    def _get_max_question_id(self, new_questions):
        return max(q.id for q in new_questions) if new_questions else self.last_id

    @log_usage()
    def _get_new_questions(self, questions):
        return [q for q in questions if q.id > self.last_id]

    @log_usage()
    def persist_state(self) -> None:
        try:
            self.storage_path.write_text(str(self.last_id))
        except IOError as e:
            self.notifier.notify(NotificationType.STATE_PERSISTING_FAILURE, e)

    @log_usage()
    async def run(self, scraper, display, db_adapter=None, interval: int = 60) -> None:  # Made async
        self.notifier.notify(NotificationType.CRAWLER_STARTED)
        try:
            await self._start_watching(scraper, display, db_adapter, interval)  # Async call
        except KeyboardInterrupt:
            self.notifier.notify(NotificationType.WATCHER_STOPPED, e=str(''))
            self.persist_state()
        except Exception as e:
            self.notifier.notify(NotificationType.WATCHER_STOPPED, e=str(e))

    @log_usage()
    async def _start_watching(self, scraper, display, db_adapter, interval):  # Made async
        while True:
            questions = scraper.scrape(max_questions=50)
            new_questions = self.watch(questions)

            if new_questions:
                self.notifier.notify(
                    NotificationType.NEW_QUESTIONS,
                    count=len(new_questions)
                )
                sorted_questions = self._sorted_questions(new_questions)
                display.display(sorted_questions)

                if db_adapter:
                    await db_adapter.insert_questions(new_questions)  # Proper async call

                self.persist_state()
            else:
                self.notifier.notify(NotificationType.NO_NEW_QUESTIONS)

            await asyncio.sleep(interval)  # Replaced time.sleep with async version

    @log_usage()
    def _sorted_questions(self, new_questions):
        return sorted(new_questions, key=lambda q: q.id)
