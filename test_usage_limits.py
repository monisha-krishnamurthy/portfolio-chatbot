import concurrent.futures
import tempfile
import unittest
from pathlib import Path
from usage_limits import reserve_request, UsageLimitError

class UsageLimitsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db = Path(self.tmp.name) / 'requests.sqlite'

    def test_minute_boundary_and_persistence(self):
        for _ in range(5):
            reserve_request(self.db, now=100)
        with self.assertRaises(UsageLimitError):
            reserve_request(self.db, now=159)
        reserve_request(self.db, now=160)

    def test_daily_boundary(self):
        for i in range(50):
            reserve_request(self.db, now=i * 61)
        with self.assertRaises(UsageLimitError):
            reserve_request(self.db, now=50 * 61)
        reserve_request(self.db, now=86400)

    def test_concurrent_reservations(self):
        def attempt(_):
            try:
                reserve_request(self.db, now=100)
                return True
            except UsageLimitError:
                return False
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
            results = list(pool.map(attempt, range(20)))
        self.assertEqual(sum(results), 5)

if __name__ == '__main__':
    unittest.main()
