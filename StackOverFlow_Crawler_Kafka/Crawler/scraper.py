# scraper.py

from .interfaces import ScraperInterface
from models import Question
from typing import List, Optional, Callable


class StackOverflowScraper_Facade(ScraperInterface):
    def __init__(self, fetcher, parser, max_questions=50):
        self.fetcher = fetcher
        self.parser = parser
        self.max_questions = max_questions

    def get_questions(self,
                      stop_condition: Optional[Callable[[Question], bool]] = None
                      ) -> List[Question]:
        questions = []
        page = 1

        while len(questions) < self.max_questions:
            html = self.fetcher.fetch(page)
            if not html:
                break

            new_questions = self.parser.parse(html)
            if not new_questions:
                break

            if stop_condition:
                filtered_questions = [q for q in new_questions if not stop_condition(q)]
                questions.extend(filtered_questions)
                if len(filtered_questions) < len(new_questions):
                    break
            else:
                questions.extend(new_questions)

            page += 1

        return questions[:self.max_questions]
