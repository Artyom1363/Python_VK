import socket
import time
import threading
import argparse
from queue import Queue
from html.parser import HTMLParser
from urllib.request import urlopen
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from worker_state import WorkerState


QUEUE_MIN_SIZE = 10


class CustomHTMLParser(HTMLParser):

    def __init__(self, mutex, most_frequent_num, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mutex = mutex
        self.words = []
        self.last_tag = ''
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.number_of_calls = 0
        self.most_common_num = most_frequent_num

    def handle_starttag(self, tag, attrs):
        self.last_tag = tag

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        bad_tags = ['script', 'meta', 'img', 'style']
        if self.last_tag in bad_tags:
            return
        new_words = self.tokenizer.tokenize(data)
        self.words.extend(new_words)

    def feed(self, data):
        super().feed(data)
        with self.mutex:
            self.number_of_calls += 1

    def get_most_common(self):
        counter = Counter(self.words)
        return dict(counter.most_common(self.most_common_num))

    def get_stat(self):
        return self.number_of_calls

    def error(self, message):
        pass


def fetch_url(url):
    with urlopen(url) as data:
        return data.read().decode()


def process_tasks(tasks, manager, parser):
    while manager.is_on():
        try:
            url, client = tasks.get(timeout=5)
            try:
                result = fetch_url(url)
                parser.feed(result)
                most_common_words = parser.get_most_common()

            except Exception:
                answer_to_client = "Error, url was not fetched"
                client.send(answer_to_client.encode())

                print("Error while processing urls in get_urls")
            else:
                answer_to_client = url + ": " + str(most_common_words)
                client.send(answer_to_client.encode())

                print("Server statistics: ",
                      f" server processed {parser.get_stat()} times!")
            finally:
                tasks.task_done()

        except Exception:
            pass


def server(tasks):
    sock = socket.socket()
    sock.bind(("", 15000))
    sock.listen(5)
    try:
        while True:
            print("WAITING...")
            client, addr = sock.accept()
            print("ACCEPTED")
            print("server: connection from", addr)

            data = client.recv(4096)

            url = data.decode()
            tasks.put((url, client))

    except KeyboardInterrupt:
        print("KeyboardInterrupt in Server")
        timeout = 2.0
        stop = time.time() + timeout
        print("Finishing tasks...")
        while tasks.unfinished_tasks and time.time() < stop:
            time.sleep(1)
        if tasks.unfinished_tasks == 0:
            print("All tasks was finished!")
        else:
            print(f"Interrupted {tasks.unfinished_tasks} unfinished tasks!")
    finally:
        sock.close()


def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', dest='workers', metavar='workers',
                        type=int, required=True)
    parser.add_argument('-k', dest='most_common_num', metavar='most common',
                        type=int, required=True)
    return parser


def batch_fetch(worker_count, parser):
    tasks_queue = Queue(maxsize=max(QUEUE_MIN_SIZE, worker_count * 2))

    worker_state = WorkerState(True)

    threads = [
        threading.Thread(target=process_tasks,
                         name=f"server_thread_{worker_num}",
                         args=(tasks_queue, worker_state, parser))
        for worker_num in range(workers_num)
    ]
    for thread in threads:
        thread.start()

    server(tasks_queue)
    worker_state.turn_off()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    arg_parser = create_argparser()
    arg_namespace = arg_parser.parse_args()
    workers_num = arg_namespace.workers
    most_common_num = arg_namespace.most_common_num
    lock = threading.Lock()
    html_parser = CustomHTMLParser(lock, most_common_num)
    batch_fetch(workers_num, html_parser)
