import asyncio
import time
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, requests_per_second: float = 1.0):
        self.rate = requests_per_second
        self.last_request_time: Dict[str, float] = {}
        self._lock = asyncio.Lock()
    
    async def acquire(self, domain: str):
        """Wait until it's safe to make another request to the domain"""
        async with self._lock:
            current_time = time.time()
            if domain in self.last_request_time:
                elapsed = current_time - self.last_request_time[domain]
                wait_time = max(0, 1.0/self.rate - elapsed)
                if wait_time > 0:
                    logger.debug(f"Rate limiting: waiting {wait_time:.2f}s for {domain}")
                    await asyncio.sleep(wait_time)
            
            self.last_request_time[domain] = time.time()
