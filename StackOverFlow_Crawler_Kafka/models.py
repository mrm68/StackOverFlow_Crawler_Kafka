# models.py

from pydantic import BaseModel
from typing import List


class Question(BaseModel):
    id: int
    title: str
    link: str
    excerpt: str
    tags: List[str]
    timestamp: str
    votes: int
    answers: int
    views: int


class Constants(BaseModel):
    user_agent: str = "Mozilla/5.0"
    base_url: str = "https://stackoverflow.com"
    tag: str = "python"
    interval: str = "3"
    retries: str = "3"
    delay: str = "2"
    max_questions: str = "50"
