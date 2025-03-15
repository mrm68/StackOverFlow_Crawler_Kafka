# models.py

from dataclasses import dataclass
from typing import List


@dataclass
class Question:
    """Data class to represent a StackOverflow question"""
    id: int
    title: str
    link: str
    excerpt: str
    tags: List[str]
    timestamp: str
