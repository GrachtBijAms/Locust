# =============================================================
#  utils/helpers.py  –  Shared helpers used by all locustfiles
# =============================================================

import random
import asyncio
from config.settings import USERS, THINK_TIME_MIN, THINK_TIME_MAX


def get_random_user() -> dict:
    """Return a random credential dict from the pool."""
    return random.choice(USERS)


async def think(min_s: float = THINK_TIME_MIN, max_s: float = THINK_TIME_MAX):
    """Async think-time pause that mimics realistic user behaviour."""
    await asyncio.sleep(random.uniform(min_s, max_s))