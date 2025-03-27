from typing import List
from .interfaces import ParserInterface
from bs4 import BeautifulSoup
from models import Question


class QuestionParser_Template_Method(ParserInterface):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def parse(self, html: str) -> List[Question]:
        soup = BeautifulSoup(html, "html.parser")
        questions = []

        for q in soup.select(".s-post-summary"):
            try:
                questions.append(self._parse_question(q))
            except Exception:
                continue

        return questions

    def _parse_question(self, q) -> Question:
        title_elem = q.select_one(".s-post-summary--content-title a")
        link = f"{self.base_url}{title_elem['href']}"

        return Question(
            id=int(title_elem['href'].split('/')[2]),
            title=title_elem.text.strip(),
            link=link,
            excerpt=q.select_one(".s-post-summary--content-excerpt").text.strip(),
            tags=[tag.text.strip() for tag in q.select(".post-tag")],
            timestamp=q.select_one(".relativetime")['title'],
            votes=int(q.select_one(".s-post-summary--stats-item:nth-child(1) span").text),
            answers=int(q.select_one(".s-post-summary--stats-item:nth-child(2) span").text),
            views=int(
                q.select_one(".s-post-summary--stats-item:nth-child(3) span").text.replace(',', ''))
        )
