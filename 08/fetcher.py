import asyncio
import aiohttp
import aiofiles


class Counter:
    def __init__(self):
        self.good = 0
        self.total = 0
        self.bad = 0


# def exception_handler(loop, context):
#     print("exception_handler was called")


async def fetch(queue, session, stat):

    while True:
        url = await queue.get()

        try:
            async with session.get(url) as resp:

                print("reading url...")
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
            print(line, type(line))
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


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # loop.set_exception_handler(exception_handler)
    # task =
    asyncio.run(batch_fetch("urls.txt"))
    # loop.run_forever()
    # print(counter)
