# fetcher.py

from .interfaces import FetcherInterface
import requests
from typing import Optional
from requests.exceptions import RequestException
import time


class Fetcher(FetcherInterface):
    """
    Strategy Pattern Implementation

    Responsibilities:
    - Handle HTTP communication with retry logic
    - Decouple fetching strategy from core logic

    Implements: FetcherInterface
    """

    def __init__(self, headers, url_builder):
        self.headers = headers
        self.url_builder = url_builder

    def fetch(self, page: int) -> Optional[str]:
        """Execute fetch operation with 3 retries"""
        for _ in range(3):
            try:
                response = requests.get(
                    self.url_builder(page),
                    headers=self.headers
                )
                response.raise_for_status()
                return response.text
            except RequestException as e:
                print(f"Error fetching page {page}: {e}")
                time.sleep(2)
        return None
