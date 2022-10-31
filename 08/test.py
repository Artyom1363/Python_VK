import unittest
# from unittest import mock
from unittest.mock import AsyncMock, Mock
from fetcher import fetch


class TestAsyncFetcher(unittest.IsolatedAsyncioTestCase):
    async def test_fetch(self):
        queue = AsyncMock()
        queue.get = AsyncMock(return_value="test_url")
        queue.task_done = Mock(side_effect=[None, None, Exception])
        session = Mock()

        good_mock = Mock()
        resp_sequence = []
        for status in [200, 300, 500]:
            resp = Mock()
            resp.status = status
            resp_sequence.append(resp)

        good_mock.__aenter__ = AsyncMock(side_effect=resp_sequence)
        good_mock.__aexit__ = AsyncMock()

        session.get = Mock(return_value=good_mock)

        stat = Mock()
        stat.total = 0
        stat.good = 0
        stat.bad = 0

        with self.assertRaises(Exception):
            await fetch(queue, session, stat)

        self.assertEqual(queue.get.call_count, 3)
        self.assertEqual(queue.task_done.call_count, 3)
        self.assertEqual(stat.total, 3)
        self.assertEqual(stat.good, 1)
        self.assertEqual(stat.bad, 2)


if __name__ == '__main__':
    unittest.main()