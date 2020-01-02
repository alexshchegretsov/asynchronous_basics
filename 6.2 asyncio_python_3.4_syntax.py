# -*- coding: utf-8 -*-
import time
import asyncio

# @asyncio.coroutine - превращает функцию в корутину


@asyncio.coroutine
def count():
    counter = 0
    while True:
        counter += 1
        print(counter)
        yield from asyncio.sleep(1)

@asyncio.coroutine
def boom():
    counter = 1
    while True:
        if not counter % 3:
            print("Boom!")
        counter += 1
        yield from asyncio.sleep(1)


@asyncio.coroutine
def main():
    task_1 = asyncio.ensure_future(count())
    task_2 = asyncio.ensure_future(boom())
    yield from asyncio.gather(task_1, task_2)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
