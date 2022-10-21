import unittest
import threading
from unittest import mock
from server import CustomHTMLParser, process_tasks, server


class TestCustomHTMLParser(unittest.TestCase):

    def setUp(self) -> None:
        with open("python3_wiki.html", "r", encoding="UTF-8") as file:
            self.data_python = file.read()

        with open("religion_wiki.html", "r", encoding="UTF-8") as file:
            self.data_religion = file.read()

    def test_custom_html_parser(self):
        lock = threading.Lock()
        parser = CustomHTMLParser(lock, 5)
        parser.feed(self.data_python)
        most_common_words = parser.get_most_common()
        self.assertEqual(len(most_common_words), 5)
        self.assertEqual(most_common_words["Python"], 453)
        self.assertEqual(most_common_words['и'], 342)
        self.assertEqual(most_common_words['в'], 327)
        self.assertEqual(most_common_words['на'], 190)
        self.assertEqual(most_common_words['с'], 172)

        parser = CustomHTMLParser(lock, 5)
        parser.feed(self.data_religion)
        most_common_words = parser.get_most_common()
        self.assertEqual(len(most_common_words), 5)
        self.assertEqual(most_common_words['и'], 381)
        self.assertEqual(most_common_words['в'], 240)
        self.assertEqual(most_common_words['религии'], 153)
        self.assertEqual(most_common_words['с'], 111)
        self.assertEqual(most_common_words['на'], 105)

        self.assertEqual(parser.get_stat(), 1)


class TestGetUrls(unittest.TestCase):

    @mock.patch("server.print")
    def test_process_tasks(self, print_mock):
        url = 'url'

        client = mock.Mock()
        client.send = mock.Mock()

        tasks_queue = mock.Mock()
        tasks_queue.get = mock.Mock(return_value=[url, client])

        worker_state = mock.Mock()
        worker_state.is_on = mock.Mock(side_effect=[True, True, False])

        html_parser = mock.Mock()
        html_parser.feed = mock.Mock()
        html_parser.get_stat = mock.Mock(return_value=2)

        html_parser.get_most_common = mock.Mock(
            side_effect=[{"word": 1}, Exception("Test")])

        with mock.patch("server.fetch_url") as fetch_url_mock:
            html_value = "<p>word<p>"
            fetch_url_mock.return_value = html_value
            process_tasks(tasks_queue, worker_state, html_parser)
            self.assertEqual(fetch_url_mock.mock_calls, [mock.call(url),
                                                         mock.call(url)])
            self.assertEqual(worker_state.is_on.call_count, 3)
            self.assertEqual(tasks_queue.mock_calls, [mock.call.get(timeout=5),
                                                      mock.call.task_done(),
                                                      mock.call.get(timeout=5),
                                                      mock.call.task_done()])
            self.assertEqual(html_parser.feed.mock_calls,
                             [mock.call(html_value),
                              mock.call(html_value)])
            self.assertEqual(html_parser.get_most_common.mock_calls,
                             [mock.call(),
                              mock.call()])
            self.assertEqual(client.send.mock_calls,
                             [mock.call(b"url: {'word': 1}"),
                              mock.call(b"Error, url was not fetched")])
            self.assertEqual(print_mock.mock_calls,
                             [mock.call("Server statistics: ",
                                        " server processed 2 times!"),
                              mock.call("Error while processing "
                              "urls in get_urls")])


class TestServer(unittest.TestCase):

    @mock.patch("socket.socket")
    @mock.patch("server.time")
    @mock.patch("server.print")
    def test_server(self, print_mock, time_mock, create_socket):
        socket = mock.Mock()
        client = mock.Mock()
        client.recv = mock.Mock(return_value=b"test url")
        address = 'address'
        socket.accept = mock.Mock(return_value=[client, address])
        tasks_queue = mock.Mock()
        tasks_queue.put = mock.Mock(side_effect=KeyboardInterrupt("test"))

        time_time_mock = mock.Mock(side_effect=[1, 2, 3])
        time_sleep_mock = mock.Mock()
        time_mock.time = time_time_mock
        time_mock.sleep = time_sleep_mock

        create_socket.return_value = socket

        server(tasks_queue)

        self.assertEqual(socket.mock_calls, [mock.call.bind(("", 15000)),
                                             mock.call.listen(5),
                                             mock.call.accept(),
                                             mock.call.close()])
        self.assertEqual(tasks_queue.mock_calls,
                         [mock.call.put(("test url", client))])
        self.assertEqual(time_time_mock.mock_calls, [mock.call(),
                                                     mock.call(),
                                                     mock.call()])
        self.assertEqual(time_sleep_mock.mock_calls, [mock.call(1)])

        self.assertEqual(print_mock.mock_calls[0:5],
                         [mock.call("WAITING..."),
                          mock.call("ACCEPTED"),
                          mock.call("server: connection from", "address"),
                          mock.call("KeyboardInterrupt in Server"),
                          mock.call("Finishing tasks...")])
        self.assertEqual(print_mock.call_count, 6)


if __name__ == '__main__':
    unittest.main()
