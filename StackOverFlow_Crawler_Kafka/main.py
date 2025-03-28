# main.py

from Crawler.fetcher import FetcherStrategy
from Crawler.parser import QuestionParserTemplateMethod
from Crawler.scraper import StackOverflowScraperFacade
from Crawler.watcher import QuestionWatcher
from Crawler.display import QuestionDisplay
from Crawler.notification_handler import Notifier
from pathlib import Path
from models import Constants


def main():
    constants = Constants()
    user_agent = constants.user_agent
    base_url = constants.base_url
    tag = constants.tag
    interval = int(constants.interval)
    retries = int(constants.interval)
    delay = int(constants.delay)
    max_questions = int(constants.max_questions)

    fetcher = FetcherStrategy(
        headers={"User-Agent": user_agent},
        url_builder=_build_url(base_url, tag),
        notifier=Notifier(),
        retries=retries,
        delay=delay
    )
    parser = QuestionParserTemplateMethod(base_url=base_url)
    scraper = StackOverflowScraperFacade(fetcher, parser, max_questions)
    watcher = QuestionWatcher(storage_path=_get_storage_path())
    display = QuestionDisplay()
    notifier = Notifier()

    watcher.run(scraper, display, notifier, interval=interval)


def _get_storage_path():
    return Path("last_seen_id_python.txt")


def _build_url(base_url, tag):
    return lambda p: f"{base_url}/questions/tagged/{tag}?page={p}"


if __name__ == "__main__":
    main()
