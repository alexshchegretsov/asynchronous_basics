# -*- coding: utf-8 -*-
from collections import deque


def gen_1(s):
    for char in s:
        yield char

def gen_2(n):
    for i in range(n):
        yield i

def round_robin_event_loop(*args):
    dq = deque(args)
    while dq:
        curr = dq.popleft()
        try:
            print(next(curr))
            dq.append(curr)
        except StopIteration:
            pass

if __name__ == '__main__':
    g1 = gen_1("alex")
    g2 = gen_2(6)
    round_robin_event_loop(g1, g2)