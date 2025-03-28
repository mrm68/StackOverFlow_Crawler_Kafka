# fetcher.py

from .interfaces import FetcherInterface
import requests
from typing import Callable, Optional
import time
import logging
from notification_handler import Notifier, NotificationType

logger = logging.getLogger(__name__)


class FetcherStrategy(FetcherInterface):
    def __init__(self, headers: dict,
                 url_builder: Callable[[int], str],
                 retries: int = 3, delay: int = 2,
                 notifier: Notifier = Notifier()):
        self.headers = headers
        self.url_builder = url_builder
        self.retries = retries
        self.delay = delay
        self.notifier = notifier

    def fetch(self, page: int) -> Optional[str]:
        for attempt in range(1, self.retries + 1):
            try:
                url = self.url_builder(page)
                self.notifier.notify(NotificationType.FETCHING_URL, url=url, attempt=attempt)
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt} failed: {e}")
                if attempt == self.retries:
                    logger.error(f"Fetch failed after {self.retries} attempts.")
                    raise RuntimeError(f"Fetch failed after {self.retries} attempts: {e}")
                time.sleep(self.delay)
        return None
