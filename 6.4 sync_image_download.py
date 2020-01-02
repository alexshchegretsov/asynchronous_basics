# -*- coding: utf-8 -*-

import requests
import time

url = "https://loremflickr.com/320/240"


def get_file(url):
    return requests.get(url=url)


def wirter(request, num):
    with open(f"image-{num}.png", "wb") as image:
        image.write(request.content)


if __name__ == '__main__':
    start = time.time()
    print(f"Started at {time.strftime('%X')}")
    for i in range(10):
        wirter(get_file(url), i)

    print(f"Finished at {time.strftime('%X')}, overall time is {time.time() - start}")

