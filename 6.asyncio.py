# -*- coding: utf-8 -*-
from collections import deque
from time import sleep

deq = deque()

def counter():
    counter = 0
    while True:
        print(counter)
        counter += 1
        yield

def printer():
    counter = 0
    while True:
        if not counter % 3:
            print("Boom!")
        counter += 1
        yield


def event_loop(deq):
    while True:
        task = deq.popleft()
        next(task)
        deq.append(task)
        sleep(0.5)

if __name__ == '__main__':

    deq.append(counter())
    deq.append(printer())

    event_loop(deq)

