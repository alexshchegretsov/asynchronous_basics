# -*- coding: utf-8 -*-
from time import sleep


def init_coro(func):
    def inner(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen

    return inner

@init_coro
def gen(first_gen):
    # this operator removes and does similarly as previous "while True" block
    res_from_sub = yield from first_gen
    sleep(1)
    print("res from sub recieved", res_from_sub)

    # while True:
    #     try:
    #         data = yield
    #         print("data from main gen", data)
    #         first_gen.send(data)
    #         sleep(1)
    #         print("send from main")
    #     except StopIteration:
    #         pass
    #     except TypeError as e:
    #         first_gen.throw(e)

@init_coro
def first_sub_gen(second_gen):
    while True:
        try:
            data = yield
            print("data from first sub_gen", data)
            second_gen.send(data)
            sleep(1)
            print("send from first")
        except StopIteration as e:
            try:
                second_gen.throw(e)
            except StopIteration as er:
                print("caught in first gen", er.value)
                return er.value
        except TypeError as e:
            print("catched type err in first on way to second sub gen")
            second_gen.throw(e)



@init_coro
def second_sub_gen():
    while True:
        try:
            data = yield
            print("data from second sub_gen", data)
        except TypeError:
            print("catched  type err in second gen")
            break
        except StopIteration:
            print("stop called in second gen")
            break
    return 78





if __name__ == '__main__':
    sec = second_sub_gen()
    first = first_sub_gen(sec)
    g = gen(first)
