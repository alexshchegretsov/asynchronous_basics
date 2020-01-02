# -*- coding: utf-8 -*-
import time
import asyncio


# @asyncio.coroutine = async def
# yield from = await


async def count():
    counter = 0
    while True:
        counter += 1
        print(counter)
        await asyncio.sleep(1)


async def boom():
    counter = 1
    while True:
        if not counter % 3:
            print("Boom!")
        counter += 1
        await asyncio.sleep(1)


async def main():
    task_1 = asyncio.create_task(count())
    task_2 = asyncio.create_task(boom())
    await asyncio.gather(task_1, task_2)


if __name__ == '__main__':
    asyncio.run(main())

