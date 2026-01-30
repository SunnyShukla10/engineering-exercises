import unittest
from src.rate_limiter import RateLimiter
from src.starter import Clock, ApiGateway


class TestRateLimiter(unittest.TestCase):
    def setUp(self):
        policies = {
            "/search": (3, 10),      # max 3 requests per 10 seconds
            "/checkout": (2, 60),    # max 2 requests per 60 seconds
        }
        self.clock = Clock(start=0)
        self.rl = RateLimiter(policies)
        self.api = ApiGateway(self.rl, self.clock)

    def test_unlimited_endpoint(self):
        # "/profile" not in policies => unlimited
        for _ in range(100):
            self.assertTrue(self.api.handle("u1", "/profile"))