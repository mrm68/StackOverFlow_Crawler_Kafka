# main.py

from Crawler.fetcher import FetcherStrategy
from Crawler.parser import QuestionParserTemplateMethod
from Crawler.scraper import StackOverflowScraperFacade
from Crawler.watcher import QuestionWatcher
from Crawler.display import QuestionDisplay
from Crawler.notification_handler import Notifier
from pathlib import Path
from models import Constants
from models import ParsConstants


def main():
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

    watcher.run(scraper, display, interval=int(constants.interval))


def _get_storage_path():
    return Path("last_seen_id_python.txt")


def _build_url(base_url, tag):
    return lambda p: f"{base_url}/questions/tagged/{tag}?page={p}"


if __name__ == "__main__":
    main()
