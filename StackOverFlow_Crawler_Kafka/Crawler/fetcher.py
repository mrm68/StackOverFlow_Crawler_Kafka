from .interfaces import FetcherInterface
import requests
from typing import Optional
import time


class Fetcher_Strategy(FetcherInterface):
    def __init__(self, headers, url_builder, retries=3, delay=2):
        self.headers = headers
        self.url_builder = url_builder
        self.retries = retries
        self.delay = delay

    def fetch(self, page: int) -> Optional[str]:
        for attempt in range(self.retries):
            try:
                response = requests.get(
                    self.url_builder(page),
                    headers=self.headers,
                    timeout=10
                )
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                if attempt == self.retries - 1:
                    raise RuntimeError(f"Failed after {self.retries} attempts: {e}")
                time.sleep(self.delay)
        return None
