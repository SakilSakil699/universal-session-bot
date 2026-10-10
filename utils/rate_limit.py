
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

In-memory rate limiter — sliding window algorithm.
"""
import time
from collections import defaultdict, deque
from typing import Deque, Dict

from config import settings


class RateLimiter:
    """
    Sliding window rate limiter.
    Tracks timestamps of recent requests per user.
    """
    
    def __init__(self, limit: int = None, window: int = 60):
        """
        limit  : max requests in window
        window : window size in seconds (default 60)
        """
        self.limit = limit or settings.RATE_LIMIT_PER_MINUTE
        self.window = window
        self._buckets: Dict[int, Deque[float]] = defaultdict(deque)
    
    def is_allowed(self, user_id: int) -> bool:
        """Check if user is under rate limit."""
        now = time.monotonic()
        bucket = self._buckets[user_id]
        
        # Drop old timestamps
        cutoff = now - self.window
        while bucket and bucket[0] < cutoff:
            bucket.popleft()
        
        # Check limit
        if len(bucket) >= self.limit:
            return False
        
        bucket.append(now)
        return True
    
    def remaining(self, user_id: int) -> int:
        """Remaining requests in current window."""
        now = time.monotonic()
        bucket = self._buckets[user_id]
        cutoff = now - self.window
        while bucket and bucket[0] < cutoff:
            bucket.popleft()
        return max(0, self.limit - len(bucket))
    
    def retry_after(self, user_id: int) -> int:
        """Seconds until next request allowed."""
        bucket = self._buckets[user_id]
        if not bucket:
            return 0
        oldest = bucket[0]
        return max(0, int(self.window - (time.monotonic() - oldest)))
    
    def reset(self, user_id: int) -> None:
        """Clear bucket for user."""
        self._buckets.pop(user_id, None)


# Global instance
rate_limiter = RateLimiter()
