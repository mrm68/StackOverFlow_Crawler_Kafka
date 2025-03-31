# main.py

from Crawler.fetcher import FetcherStrategy
from Crawler.parser import QuestionParserTemplateMethod
from Crawler.scraper import StackOverflowScraperFacade
from Crawler.watcher import QuestionWatcher
from Crawler.display import QuestionDisplay
from Crawler.notification_handler import Notifier
from pathlib import Path
from models import Constants, ParsConstants
import os
import asyncio  # Added for async main
from Crawler.db_adapter import PostgresAdapter


def initiate_kafka():
    print("✅ Starting crawler with config:")
    print(f"Kafka: {os.getenv('KAFKA_BOOTSTRAP_SERVERS')}")
    print(f"Topic: {os.getenv('KAFKA_TOPIC')}")
    print(f"Interval: {os.getenv('SCRAPE_INTERVAL', '60')}s")


async def main():  # Made async
    initiate_kafka()
    constants = Constants()
    notifier_object = Notifier()
    fetcher = FetcherStrategy(
        headers={"User-Agent": constants.user_agent},
        url_builder=_build_url(constants.base_url, constants.tag),
        notifier=notifier_object,
        retries=int(constants.interval),
        delay=int(constants.delay)
    )
    parser = QuestionParserTemplateMethod(base_url=constants.base_url,
                                          parse_constants=ParsConstants(),
                                          notifier=notifier_object)
    scraper = StackOverflowScraperFacade(fetcher, parser, notifier=notifier_object,
                                         max_questions=int(constants.max_questions))
    watcher = QuestionWatcher(storage_path=_get_storage_path(), notifier=notifier_object)
    display = QuestionDisplay()

    db_adapter = PostgresAdapter()
    await db_adapter.init()  # Async init

    # Run the async watcher
    await watcher.run(scraper, display, db_adapter=db_adapter, interval=int(constants.interval))


def _get_storage_path():
    return Path("last_seen_id_python.txt")


def _build_url(base_url, tag):
    return lambda p: f"{base_url}/questions/tagged/{tag}?page={p}"


if __name__ == "__main__":
    asyncio.run(main())  # Proper async entry point
