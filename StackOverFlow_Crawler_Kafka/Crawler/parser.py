# parser.py

from .interfaces import ParserInterface
from bs4 import BeautifulSoup
from models import Question, ParsConstants
from typing import List
from .notification_handler import NotificationType, Notifier
from .tracedecorator import log_usage


class QuestionParserTemplateMethod(ParserInterface):
    @log_usage()
    def __init__(self, base_url: str,
                 notifier: Notifier, parse_constants: ParsConstants):
        self.base_url = base_url
        self.parse_constants = parse_constants
        self.notifier = notifier or Notifier()

    @log_usage()
    def parse(self, html: str) -> List[Question]:
        soup = BeautifulSoup(html, "html.parser")
        results = []
        for q in soup.select(self.parse_constants.post_summary):
            link_elem = q.select_one(self.parse_constants.post_title)
            if not link_elem:
                continue
            try:
                qid = self._extract_questionID(link_elem)
            except (IndexError, ValueError) as e:
                self.notifier.notify(NotificationType.QUESTION_PARSE_ERROR, qid=str(qid), e=e)
                continue

            excerpt_elem = q.select_one(self.parse_constants.excerpt_elem)
            timestamp_elem = q.select_one(self.parse_constants.timestamp_elem)
            vote_elem = q.select_one(self.parse_constants.vote_elem)
            answer_elem = q.select_one(self.parse_constants.answer_elem)
            view_elem = q.select_one(self.parse_constants.view_elem)
            item = Question(
                id=qid,
                title=self._extract_title(link_elem),
                link=self._extract_link(link_elem),
                excerpt=self._extract_excerpt(excerpt_elem),
                tags=self._extract_questionTags(q),
                timestamp=self._extract_timestamp(timestamp_elem),
                votes=self._extract_votesCount(vote_elem),
                answers=self._extracts_answersCount(answer_elem),
                views=self._extract_viewsCount(view_elem)
            )
            results.append(item)
        return results

    def _extract_questionID(self, link_elem):
        return int(link_elem['href'].split('/')[2])

    def _extract_title(self, link_elem):
        return link_elem.text.strip()

    def _extract_link(self, link_elem):
        return f"{self.base_url}{link_elem['href']}"

    def _extract_excerpt(self, excerpt_elem):
        return excerpt_elem.text.strip() if excerpt_elem else ""

    def _extract_timestamp(self, timestamp_elem):
        return timestamp_elem['title'] if timestamp_elem and timestamp_elem.has_attr(
            'title') else ""

    def _extract_questionTags(self, q):
        return [tag.text.strip() for tag in q.select(".post-tag")]

    def _extract_viewsCount(self, view_elem):
        return int(view_elem.text.strip().replace(',', '')
                   ) if view_elem and view_elem.text.strip().replace(',', '').isdigit() else 0

    def _extracts_answersCount(self, answer_elem):
        return int(answer_elem.text.strip()
                   ) if answer_elem and answer_elem.text.strip().isdigit() else 0

    def _extract_votesCount(self, vote_elem):
        return int(vote_elem.text.strip()
                   ) if vote_elem and vote_elem.text.strip().isdigit() else 0
