import unittest
from unittest import mock
from unittest.mock import AsyncMock, Mock, patch
from fetcher import fetch, batch_fetch


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

    @patch('fetcher.print')
    @patch('aiohttp.ClientSession', new_callable=Mock)
    async def test_batch_fetch(self, client_session, print_mock):

        good_mock = Mock()
        resp_sequence = []
        for status in [200, 200, 200, 200, 200, 500]:
            resp = Mock()
            resp.status = status
            resp_sequence.append(resp)

        good_mock.__aenter__ = AsyncMock(side_effect=resp_sequence)
        good_mock.__aexit__ = AsyncMock()

        session = Mock()
        session.get = Mock(return_value=good_mock)

        get_session = Mock()
        get_session.__aenter__ = AsyncMock(return_value=session)
        get_session.__aexit__ = AsyncMock()

        client_session.return_value = get_session
        await batch_fetch("test_urls.txt", workers_count=3, queue_size=5)
        self.assertEqual(good_mock.__aenter__.call_count, 6)
        self.assertEqual(good_mock.__aexit__.call_count, 6)
        self.assertEqual(session.get.call_count, 6)
        self.assertEqual(session.get.mock_calls, [
            mock.call.get('https:Python1\n'),
            mock.call.get('https:Python2\n'),
            mock.call.get('https:Python3\n'),
            mock.call.get('https:Python4\n'),
            mock.call.get('https:Python5\n'),
            mock.call.get('https:Python6\n')])

        self.assertEqual(print_mock.mock_calls, [
            mock.call.get('Fetch url... status: 200'),
            mock.call.get('Fetch url... status: 200'),
            mock.call.get('Fetch url... status: 200'),
            mock.call.get('Fetch url... status: 200'),
            mock.call.get('Fetch url... status: 200'),
            mock.call.get('Fetch url... status: 500'),
            mock.call.get('statistics.good=5'),
            mock.call.get('statistics.total=6')
        ])


if __name__ == '__main__':
    unittest.main()
