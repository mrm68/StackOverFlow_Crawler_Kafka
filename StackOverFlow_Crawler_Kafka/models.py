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


class ParsConstants(BaseModel):
    post_summary: str = ".s-post-summary"
    post_title: str = ".s-post-summary--content-title a"
    excerpt_elem: str = ".s-post-summary--content-excerpt"
    timestamp_elem: str = ".relativetime"
    vote_elem: str = ".s-post-summary--stats-item:nth-child(1) span"
    answer_elem: str = ".s-post-summary--stats-item:nth-child(2) span"
    view_elem: str = ".s-post-summary--stats-item:nth-child(3) span"
