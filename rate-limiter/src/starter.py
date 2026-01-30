from src.rate_limiter import RateLimiter
from src.models import Request
class Clock:
    def __init__(self, start: int = 0):
        self._t = start

    def now(self) -> int:
        return self._t

    def advance(self, seconds: int):
        self._t += seconds


class ApiGateway:
    def __init__(self, rate_limiter: "RateLimiter", clock: Clock):
        self.rate_limiter = rate_limiter
        self.clock = clock

    def handle(self, user_id: str, endpoint: str) -> bool:
        """
        Returns:
            True  -> request allowed
            False -> request blocked (rate limited)
        """
        req = Request(user_id=user_id, endpoint=endpoint, timestamp=self.clock.now())
        return self.rate_limiter.allow(req)
