import socket
import threading
import argparse
from queue import Queue
from worker_state import WorkerState


QUEUE_MAX_SIZE = 10


def client(queue, manager):
    while manager.is_on():
        try:
            url = queue.get(timeout=2)
            print(url)
            sock = socket.socket()
            sock.connect(("", 15000))
            sock.sendall(url.encode())
            data = sock.recv(1024)
            print("client:", data.decode())
        except Exception:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(dest='threads', metavar='Threads', type=int,
                        help='Number of threads')
    parser.add_argument(dest='urls_filename', metavar='urls_filename',
                        type=str, help='Filename with urls')

    namespace = parser.parse_args()
    threads_number = namespace.threads
    file_with_urls = namespace.urls_filename
    urls_queue = Queue(maxsize=QUEUE_MAX_SIZE)
    worker_state = WorkerState(True)

    threads = [
        threading.Thread(target=client,
                         name=f"client_thread_{thread_num}",
                         args=(urls_queue, worker_state))
        for thread_num in range(threads_number)
    ]

    for thread in threads:
        thread.start()

    with open(file_with_urls, "r") as file:
        for url in file:
            # print(f"{url=}")
            urls_queue.put(url)

    worker_state.turn_off()

    for thread in threads:
        thread.join()
