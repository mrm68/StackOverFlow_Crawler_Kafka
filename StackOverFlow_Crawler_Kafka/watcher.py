# watcher.py

import time
from pathlib import Path
from scraper import StackOverflowScraper
from display import QuestionDisplay


class QuestionWatcher:
    """Service to monitor for new StackOverflow questions."""

    def __init__(self, language: str, check_interval: int = 60):
        self.language = language
        self.check_interval = check_interval
        self.scraper = StackOverflowScraper(language=language, max_questions=500)
        self.last_seen_id = self._load_last_seen_id()

    def _load_last_seen_id(self) -> int:
        path = self._get_storage_path()
        if path.exists():
            try:
                with open(path, 'r') as f:
                    return int(f.read().strip())
            except (ValueError, IOError):
                return 0
        else:
            try:
                questions = self.scraper.get_questions()
                if questions:
                    # Skip invalid IDs
                    max_id = max(q.id for q in questions if q.id != 0)
                    self._save_last_seen_id(max_id)
                    return max_id
                return 0
            except Exception as e:
                print(f"Error initializing last seen ID: {e}")
                return 0

    def _save_last_seen_id(self, last_id: int):
        with open(self._get_storage_path(), 'w') as f:
            f.write(str(last_id))

    def _get_storage_path(self):
        return Path(f"last_seen_id_{self.language}.txt")

    def start_watching(self):
        """Start the monitoring service."""
        print(
            f"🚀 Starting watcher for '{self.language}'. "
            f"Checking every {self.check_interval} seconds."
        )
        print("Press Ctrl+C to stop...")
        try:
            while True:
                self.check_new_questions()
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            print("\n🛑 Watcher stopped.")

    def check_new_questions(self):
        """Check for new questions and notify."""
        def stop_condition(q): return q.id <= self.last_seen_id
        questions = self.scraper.get_questions(stop_condition=stop_condition)
        new_questions = [q for q in questions if q.id > self.last_seen_id]

        if new_questions:
            new_questions_sorted = sorted(new_questions, key=lambda q: q.id)
            max_id = new_questions_sorted[-1].id
            self.last_seen_id = max_id
            self._save_last_seen_id(max_id)
            print(f"\n🔔 Found {len(new_questions)} new questions:")
            QuestionDisplay.display(new_questions_sorted)
        else:
            print(
                f"⏳ No new questions found. Last check: "
                f"{time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
