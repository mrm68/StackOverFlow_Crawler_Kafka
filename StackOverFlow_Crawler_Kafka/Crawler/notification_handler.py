# notification_handler.py
import logging
from enum import Enum, auto
import time


class NotificationType(Enum):
    WATCHER_STARTED = auto()
    WATCHER_STOPPED = auto()
    NEW_QUESTIONS = auto()
    NO_NEW_QUESTIONS = auto()
    CRAWLER_STARTED = auto()
    FOUND_QUESTIONS = auto()
    FETCHING_URL = auto()


class Notifier:
    def __init__(self):
        # Mapping of notification types to handler methods.
        self._handlers = {
            NotificationType.WATCHER_STARTED: self._handle_watcher_started,
            NotificationType.WATCHER_STOPPED: self._handle_watcher_stopped,
            NotificationType.NEW_QUESTIONS: self._handle_new_questions,
            NotificationType.NO_NEW_QUESTIONS: self._handle_no_questions,
            NotificationType.CRAWLER_STARTED: self._handle_crawler_started,
            NotificationType.FOUND_QUESTIONS: self._handle_found_questions,
            NotificationType.FETCHING_URL: self._handle_fetching_url,
        }
        self.logger = logging.getLogger(__name__)

    def notify(self, notification_type: NotificationType, **kwargs):
        handler = self._handlers.get(notification_type)
        if handler:
            handler(**kwargs)
        else:
            print(f"⚠️ Unhandled notification type: {notification_type}")

    def _handle_fetching_url(self, url: str, attempt: str):
        print(f"Fetching URL: {url} (Attempt {attempt})")
        self.logger.info(f"Fetching URL: {url} (Attempt {attempt})")

    def _handle_found_questions(self, questions_count: int):
        print(f"✅ Found {questions_count} initial questions")

    def _handle_crawler_started(self):
        print("🚀 Starting initial crawl...")

    def _handle_watcher_started(self, language: str, interval: int):
        print(f"🚀 Watching '{language}', checking every {interval} seconds.")

    def _handle_watcher_stopped(self):
        print("\n🛑 Watcher stopped.")

    def _handle_new_questions(self, count: int):
        print(f"\n🔔 Found {count} new questions:")

    def _handle_no_questions(self):
        print(f"⏳ No new questions. Last check: {time.strftime('%Y-%m-%d %H:%M:%S')}")
