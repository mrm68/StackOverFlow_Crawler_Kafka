from enum import Enum, auto
import time


class NotificationType(Enum):
    WATCHER_STARTED = auto()
    WATCHER_STOPPED = auto()
    NEW_QUESTIONS = auto()
    NO_NEW_QUESTIONS = auto()


class Notifier:
    def __init__(self):
        # Map enum members to their handler methods
        self._handlers = {
            NotificationType.WATCHER_STARTED: self._handle_watcher_started,
            NotificationType.WATCHER_STOPPED: self._handle_watcher_stopped,
            NotificationType.NEW_QUESTIONS: self._handle_new_questions,
            NotificationType.NO_NEW_QUESTIONS: self._handle_no_questions,
        }

    def notify(self, notification_type: NotificationType, **kwargs):
        """Main notification interface"""
        handler = self._handlers.get(notification_type)
        if handler:
            handler(**kwargs)
        else:
            print(f"⚠️ Unhandled notification type: {notification_type}")

    # Delegate methods
    def _handle_watcher_started(self, language: str, interval: int):
        print(f"🚀 Starting watcher for '{language}'. Checking every {interval} seconds.")
        print("Press Ctrl+C to stop...")

    def _handle_watcher_stopped(self):
        print("\n🛑 Watcher stopped.")

    def _handle_new_questions(self, count: int):
        print(f"\n🔔 Found {count} new questions:")

    def _handle_no_questions(self):
        print(f"⏳ No new questions found. Last check: {time.strftime('%Y-%m-%d %H:%M:%S')}")
