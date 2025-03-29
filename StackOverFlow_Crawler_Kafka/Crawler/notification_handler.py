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
    FETCH_FAILED = auto()
    NO_HTML_PARSED = auto()
    NO_QUESTIONS_PARSED = auto()
    STREAMING_ERROR = auto()
    STATE_LOADING_FAILURE = auto()
    STATE_PERSISTING_FAILURE = auto()
    QUESTION_PARSE_ERROR = auto()


class Notifier:
    def __init__(self):
        # Mapping of notification types to handler methods.
        self._handlers = {
            NotificationType.WATCHER_STARTED: self._handle_watcher_started,
            NotificationType.WATCHER_STOPPED: self._handle_watcher_stopped,
            NotificationType.NEW_QUESTIONS: self._handle_new_questions,
            NotificationType.NO_NEW_QUESTIONS: self._handle_no_new_questions,
            NotificationType.CRAWLER_STARTED: self._handle_crawler_started,
            NotificationType.FOUND_QUESTIONS: self._handle_found_questions,
            NotificationType.FETCHING_URL: self._handle_fetching_url,
            NotificationType.FETCH_FAILED: self._handle_fetch_failed,
            NotificationType.NO_HTML_PARSED: self._handle_no_html_parsed,
            NotificationType.NO_QUESTIONS_PARSED: self._handle_no_questions_parsed,
            NotificationType.QUESTION_PARSE_ERROR: self._handle_question_parse_error,
            NotificationType.STREAMING_ERROR: self._handle_streaming_error,
            NotificationType.STATE_LOADING_FAILURE: self._handle_state_loading_failure,
            NotificationType.STATE_PERSISTING_FAILURE: self._handle_state_persisting_failure,


        }
        self.logger = logging.getLogger(__name__)

    def notify(self, notification_type: NotificationType, **kwargs):
        handler = self._handlers.get(notification_type)
        if handler:
            handler(**kwargs)
        else:
            print(f"⚠️ Unhandled notification type: {notification_type}")

    def _handle_question_parse_error(self, e: str, qid: str):
        print((f"⚠️ Parsing Question Error, Question ID={qid}: {e.title}"))
        self.logger.warning(f"Failed to parse question ID: {e}")

    def _handle_state_persisting_failure(self, e: str):
        self.logger.error(f"Failed to persist state: {e}")
        print((f"⚠️ Failed to persist state: {e.title}"))
        raise

    def _handle_state_loading_failure(self, e: str):
        self.logger.warning(f"State load failed: {e}")
        print((f"⚠️ State load failed: {e.title}"))

    def _handle_streaming_error(self, e: str):
        self.logger.error(f"Error while streaming questions: {e}")
        print((f"⚠️ Error while streaming questions: {e.title}"))

    def _handle_no_questions_parsed(self):
        self.logger.info("No questions parsed, ending scrape.")
        print("No questions parsed, ending scrape.")

    def _handle_no_html_parsed(self):
        self.logger.info("No HTML returned, ending scrape.")
        print("⚠️ No HTML returned, ending scrape.")

    def _handle_fetch_failed(self, retries: str, e: str):
        print(f"⚠️ Fetch failed after {retries} attempts.")
        self.logger.error(f"Fetch failed after {retries} attempts.")
        raise RuntimeError(f"Fetch failed after {retries} attempts: {e}")

    def _handle_fetching_url(self, url: str, attempt: str):
        print(f"Fetching URL: {url} (Attempt {attempt})")
        self.logger.info(f"Fetching URL: {url} (Attempt {attempt})")

    def _handle_found_questions(self, questions_count: int):
        print(f"✅ Found {questions_count} initial questions")

    def _handle_crawler_started(self):
        print("🚀 Starting initial crawl...")

    def _handle_watcher_started(self, language: str, interval: int):
        print(f"🚀 Watching '{language}', checking every {interval} seconds.")

    def _handle_watcher_stopped(self, e: str):
        print("\n🛑 Watcher stopped.")
        self.logger.error(f"Watcher encountered an error: {e}")
        raise

    def _handle_new_questions(self, count: int):
        print(f"\n🔔 Found {count} new questions:")

    def _handle_no_new_questions(self):
        print(f"⏳ No new questions. Last check: {time.strftime('%Y-%m-%d %H:%M:%S')}")
