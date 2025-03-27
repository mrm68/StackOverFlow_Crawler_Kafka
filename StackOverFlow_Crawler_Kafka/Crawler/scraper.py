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

            page_questions = self.parser.parse(html)
            if not page_questions:
                break

            if stop_condition:
                filtered = [q for q in page_questions if not stop_condition(q)]
                questions.extend(filtered)
                if len(filtered) < len(page_questions):
                    break
            else:
                questions.extend(page_questions)

            page += 1

        return questions[:self.max_questions]
