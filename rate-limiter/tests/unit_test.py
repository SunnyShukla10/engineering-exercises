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
    
    def test_simple_limit(self):
        # 3 allowed, 4th blocked within 10 seconds
        self.assertTrue(self.api.handle("u1", "/search"))  # t=0
        self.assertTrue(self.api.handle("u1", "/search"))  # t=0
        self.assertTrue(self.api.handle("u1", "/search"))  # t=0
        self.assertFalse(self.api.handle("u1", "/search")) # t=0

    def test_blocked_does_not_count(self):
        # hit limit
        self.assertTrue(self.api.handle("u1", "/search"))
        self.assertTrue(self.api.handle("u1", "/search"))
        self.assertTrue(self.api.handle("u1", "/search"))
        self.assertFalse(self.api.handle("u1", "/search"))

        # advance time so oldest expires
        self.clock.advance(10)  # window boundary
        # now should allow again
        self.assertTrue(self.api.handle("u1", "/search"))