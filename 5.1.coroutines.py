# -*- coding: utf-8 -*-


# инициализация генератора
def coroutine(func):
    def inner(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen

    return inner


@coroutine
def simple_coroutine():
    while True:
        x = "yielded each time"
        message = yield x
        print("recieved", message)


@coroutine
def average():
    count = 0
    summ = 0
    avg = None
    while True:
        try:
            x = yield avg
        except StopIteration:
            print("done")
            break
        else:
            count += 1
            summ += x
            avg = round(summ / count, 2)
    # return возвращает навсегда управление из генератора
    # забросив исключение в корутину,
    # значение avg можно получить через атрибут value у пойманного исключения
    return avg


"""
>>> try:
...     g.throw(StopIteration)
... except StopIteration as e:
...     print("average is", e.value)
... 
done
average is 29.33

"""
