# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import time

url = "https://loremflickr.com/320/240"

async def get_content(session, url, i):
    async with session.get(url, allow_redirects=True) as response:
        content = await response.read()
        # use sync function
        write_image(content, i)

# sync function
def write_image(content, num):
    with open(f"image-{num}.png", "wb") as image:
        image.write(content)

async def main():
    start = time.time()
    print(f"Started at {time.strftime('%X')}")
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(10):
            task = asyncio.create_task( get_content(session, url, i) )
            tasks.append(task)
        await asyncio.gather(*tasks)
    print(f"Finished at {time.strftime('%X')}, overall time is {time.time() - start}")


if __name__ == '__main__':
    asyncio.run(main())