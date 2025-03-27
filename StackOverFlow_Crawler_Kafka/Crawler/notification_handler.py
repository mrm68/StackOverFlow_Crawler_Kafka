# notification_handler.py

from enum import Enum, auto
import time


class NotificationType(Enum):
    WATCHER_STARTED = auto()
    WATCHER_STOPPED = auto()
    NEW_QUESTIONS = auto()
    NO_NEW_QUESTIONS = auto()


class Notifier:
    def __init__(self):
        self._handlers = {
            NotificationType.WATCHER_STARTED: self._handle_watcher_started,
            NotificationType.WATCHER_STOPPED: self._handle_watcher_stopped,
            NotificationType.NEW_QUESTIONS: self._handle_new_questions,
            NotificationType.NO_NEW_QUESTIONS: self._handle_no_questions,
        }

    def notify(self, notification_type: NotificationType, **kwargs):
        handler = self._handlers.get(notification_type)
        if handler:
            handler(**kwargs)
        else:
            print(f"⚠️ Unhandled notification type: {notification_type}")

    def _handle_watcher_started(self, language: str, interval: int):
        print(f"🚀 Watching '{language}', checking every {interval} seconds.")

    def _handle_watcher_stopped(self):
        print("\n🛑 Watcher stopped.")

    def _handle_new_questions(self, count: int):
        print(f"\n🔔 Found {count} new questions:")

    def _handle_no_questions(self):
        print(f"⏳ No new questions. Last check: {time.strftime('%Y-%m-%d %H:%M:%S')}")
