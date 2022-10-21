import multiprocessing
import socket
import time
import threading
import argparse
import sys
from queue import Queue
from html.parser import HTMLParser
from urllib.request import urlopen
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from time import time


running = False


class CustomHTMLParser(HTMLParser):
    number_of_calls = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.words = []
        self.last_tag = ''
        self.tokenizer = RegexpTokenizer(r'\w+')

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

    def feed_with_counter(self, data, lock):
        super().feed(data)
        with lock:
            CustomHTMLParser.number_of_calls += 1

    def get_most_common(self, quantity=10):
        counter = Counter(self.words)
        return dict(counter.most_common(quantity))

    @staticmethod
    def get_most_common_all(quantity=10):
        counter = Counter(CustomHTMLParser.common_words)
        return dict(counter.most_common(quantity))


def fetch_url(url):
    resp = urlopen(url)
    return resp.read().decode()


def get_urls(queue_, lock):
    while running:
        try:
            url, client = queue_.get(timeout=1)
            # print(f"Got task from Queue, rest of tasks: COUNT {queue_.qsize()}\n", end="")
            try:
                result = fetch_url(url)
                html_parser = CustomHTMLParser()
                html_parser.feed_with_counter(result, lock)
                most_common_words = html_parser.get_most_common(5)
                # print(f" words: {most_common_words}")
            except Exception:
                answer_to_client = "Error, url was not fetched"
                # print("Everything good!", f"{answer_to_client=}")
                client.send(answer_to_client.encode())
                print("Error while processing urls in get_urls")
            else:
                answer_to_client = url + ": " + str(most_common_words)
                # print("Everything good!", f"{answer_to_client=}")
                client.send(answer_to_client.encode())
            finally:
                # print("finally in get urls")
                queue_.task_done()

        except Exception:
            pass


def server(queue_):
    sock = socket.socket()
    sock.bind(("", 15000))
    sock.listen(5)
    # global running
    # running = True
    try:
        while True:
            print("WAITING...")
            client, addr = sock.accept()
            print("ACCEPTED")
            print("server: conn from", addr)

            # data = b""
            data = client.recv(4096)
            # while (chunk := client.recv(1024)):
            #     data += chunk

            url = data.decode()
            queue_.put((url, client))

            # print("server:", data)
            # client.send(data.upper())
    except KeyboardInterrupt:
        print("KeyboardInterrupt in Server")
        timeout = 2.0
        stop = time() + timeout
        print("Finishing tasks...")
        # print(f"{tasks_queue.unfinished_tasks=}")
        while tasks_queue.unfinished_tasks and time() < stop:
            time.sleep(1)
            print(f"{time=}, {stop=}")
        if tasks_queue.unfinished_tasks == 0:
            print("All tasks was finished!")
        else:
            print(f"Interrupted {tasks_queue.unfinished_tasks} unfinished tasks!")
    finally:
        # print("Some error in server")
        sock.close()
        # tasks_queue.join()
        # running = False
        return


def create_argparser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-w', dest='workers', metavar='workers', type=int, required=True)
    arg_parser.add_argument('-k', dest='most_common_quan', metavar='most common', type=int, required=True)
    return arg_parser


if __name__ == "__main__":
    arg_parser = create_argparser()
    arg_namespace = arg_parser.parse_args()
    workers_num = arg_namespace.workers
    # args = vars(args)
    tasks_queue = Queue()
    lock = threading.Lock()
    threads = [
        threading.Thread(target=get_urls, name=f"server_thread_{worker_num}", args=(tasks_queue, lock))
        for worker_num in range(workers_num)
    ]
    running = True
    for thread in threads:
        thread.start()

    server(tasks_queue)
    running = False
