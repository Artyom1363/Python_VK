import multiprocessing
import socket
import time
import threading
import argparse
from queue import Queue


def client(queue):
    while True:
        try:
            url = queue.get(timeout=2)
            print(url)
            sock = socket.socket()
            sock.connect(("", 15000))
            sock.sendall(url.encode())
            data = sock.recv(1024)
            print("client:", data.decode())
        except Exception:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(dest='threads', metavar='Threads', type=int,
                        help='Number of threads')
    parser.add_argument(dest='urls_filename', metavar='urls_filename', type=str,
                        help='Filename with urls')

    namespace = parser.parse_args()
    threads_number = namespace.threads
    file_with_urls = namespace.urls_filename
    urls_queue = Queue()

    with open(file_with_urls, "r") as file:
        for url in file:
            # print(f"{url=}")
            urls_queue.put(url)

    threads = [
        threading.Thread(target=client, name=f"client_thread_{thread_num}", args=(urls_queue,))
        for thread_num in range(threads_number)
    ]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
