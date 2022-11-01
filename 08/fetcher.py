import asyncio
import argparse
import aiohttp
import aiofiles


class Counter:
    def __init__(self):
        self.good = 0
        self.total = 0
        self.bad = 0


async def fetch(queue, session, stat):

    while True:
        url = await queue.get()

        try:
            async with session.get(url) as resp:

                print(f"Fetch url... status: {resp.status}")
                if resp.status == 200:
                    stat.good += 1
                else:
                    stat.bad += 1
        finally:
            stat.total += 1
            queue.task_done()


async def filling_queue(queue, filename):
    async with aiofiles.open(filename, "r") as file:
        async for line in file:
            # print(line, type(line))
            await queue.put(line)


async def batch_fetch(filename, workers_count=5, queue_size=10):
    tasks = asyncio.Queue(queue_size)
    filling_urls = asyncio.create_task(filling_queue(tasks, filename))
    # await filling_urls
    # time.sleep(1)
    statistics = Counter()
    async with aiohttp.ClientSession() as session:
        workers = [
            asyncio.create_task(fetch(tasks, session, statistics))
            for _ in range(workers_count)
        ]
        await filling_urls
        await tasks.join()
        # await asyncio.wait(workers, return_when=asyncio.ALL_COMPLETED)
        for worker in workers:
            worker.cancel()

    print(f"{statistics.good=}")
    print(f"{statistics.total=}")


def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='workers', metavar='workers', type=int)
    parser.add_argument(dest='args', metavar='filename', nargs='+')
    return parser


if __name__ == "__main__":
    arg_parser = create_argparser()
    arg_namespace = arg_parser.parse_args()
    if vars(arg_namespace)["workers"] is not None:
        workers_num = vars(arg_namespace)["workers"]
        filename_with_urls = vars(arg_namespace)["args"][0]
    else:
        workers_num, filename_with_urls = vars(arg_namespace)["args"]
        workers_num = int(workers_num)

    # print(f"{workers_num=}, {filename}")

    loop = asyncio.get_event_loop()
    asyncio.run(batch_fetch("urls.txt", workers_num, filename_with_urls))
