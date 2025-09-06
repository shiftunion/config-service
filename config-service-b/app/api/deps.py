"""
API dependencies.
"""
from app.db import pool


async def get_db_connection():
    """Get database connection dependency."""
    async with pool.get_connection() as conn:
        yield conn
