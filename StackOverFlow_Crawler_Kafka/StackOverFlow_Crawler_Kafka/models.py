# models.py

from pydantic import BaseModel
from typing import List


class Question(BaseModel):
    """Pydantic model to represent a StackOverflow question"""
    id: int
    title: str
    link: str
    excerpt: str
    tags: List[str]
    timestamp: str
    votes: int
    answers: int
    views: int
