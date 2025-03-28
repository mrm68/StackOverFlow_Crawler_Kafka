# parser.py

from .interfaces import ParserInterface
from bs4 import BeautifulSoup
from models import Question
from typing import List
import logging

logger = logging.getLogger(__name__)


class QuestionParserTemplateMethod(ParserInterface):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def parse(self, html: str) -> List[Question]:
        soup = BeautifulSoup(html, "html.parser")
        results = []
        for q in soup.select(".s-post-summary"):
            link_elem = q.select_one(".s-post-summary--content-title a")
            if not link_elem:
                continue
            try:
                # Extract the question ID robustly
                qid = int(link_elem['href'].split('/')[2])
            except (IndexError, ValueError) as e:
                logger.warning(f"Failed to parse question ID: {e}")
                continue

            excerpt_elem = q.select_one(".s-post-summary--content-excerpt")
            timestamp_elem = q.select_one(".relativetime")
            vote_elem = q.select_one(".s-post-summary--stats-item:nth-child(1) span")
            answer_elem = q.select_one(".s-post-summary--stats-item:nth-child(2) span")
            view_elem = q.select_one(".s-post-summary--stats-item:nth-child(3) span")
            item = Question(
                id=qid,
                title=link_elem.text.strip(),
                link=f"{self.base_url}{link_elem['href']}",
                excerpt=excerpt_elem.text.strip() if excerpt_elem else "",
                tags=[tag.text.strip() for tag in q.select(".post-tag")],
                timestamp=timestamp_elem['title'] if timestamp_elem and timestamp_elem.has_attr(
                    'title') else "",
                votes=int(vote_elem.text.strip()
                          ) if vote_elem and vote_elem.text.strip().isdigit() else 0,
                answers=int(answer_elem.text.strip()
                            ) if answer_elem and answer_elem.text.strip().isdigit() else 0,
                views=int(view_elem.text.strip().replace(',', '')
                          ) if view_elem and view_elem.text.strip().replace(',', '').isdigit() else 0
            )
            results.append(item)
        return results
