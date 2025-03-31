# db_adapter.py

import asyncpg
import os
from .tracedecorator import log_usage


class PostgresAdapter:
    @log_usage()
    def __init__(self, dsn: str = None):
        self.dsn = dsn or os.getenv('DATABASE_DSN', 'postgresql://user:password@localhost:5432/mydb')
        self.pool = None

    @log_usage()
    async def init(self):
        """Initialize the database connection pool."""
        self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=1, max_size=10)
        await self._create_table()

    @log_usage()
    async def _create_table(self):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS questions (
                    id BIGINT PRIMARY KEY,
                    title TEXT,
                    link TEXT,
                    excerpt TEXT,
                    tags TEXT[],
                    timestamp TEXT,
                    votes INTEGER,
                    answers INTEGER,
                    views INTEGER
                );
            ''')

    @log_usage()
    async def insert_questions(self, questions):
        """Batch insert questions using executemany"""
        if not questions:
            return

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.executemany('''
                    INSERT INTO questions
                    (id, title, link, excerpt, tags, timestamp, votes, answers, views)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                    ON CONFLICT (id) DO NOTHING;
                ''', [
                    (q.id, q.title, q.link, q.excerpt, q.tags,
                     q.timestamp, q.votes, q.answers, q.views)
                    for q in questions
                ])

    @log_usage()
    async def close(self):
        """Close the connection pool properly."""
        if self.pool:
            await self.pool.close()
