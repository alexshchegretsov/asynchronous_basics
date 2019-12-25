# -*- coding: utf-8 -*-

# yield from выдаёт значения из любого итератора
# yield from "alex"
# yield from [1, 2, 3, 4]

# инициализация генератора
def coroutine(func):
    def inner(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen

    return inner


def subgen():
    while True:
        try:
            m = yield
        # any exception
        except (TypeError, StopIteration):
            print("Stopped")
            break
        else:
            print("recieved from delegator", m)
    return "returned from subgenerator"


# yield from берёт на себя передачу данных в подгенератор,
# передачу исключений, получает с помощью return возвращаемый результат,
# который можно дополнительно обработать
# используя синтаксис yield from gen и метод send()
# мы можем пробрасывать информацию в подгенератор - она запишется в переменную "m"
# yield from автоматически инициализирует подгенератор
# yeild from автоматичеки перехватывает return и возвращаемое значение из подгенератора,
# записывая в переменную returned_from_subgen


@coroutine
def delegator(gen):
    returned_from_subgen = yield from gen
    print(returned_from_subgen)


# yield from в других языках называется await
# и смысл его заключается в том, что вызывающий код
# напрямую управляет работой подгенератора
# и пока это происходит - делегирующий генератор остаётся заблокированным
# тоесть он вынужден ожидать, AWAIT, когда подгенератор закончит свою работу
# но здесь есть важная деталь, подгенератор должен содержать в себе
# механизм, завершающий его работу, и если этого не сделать -
# то делегирующий генератор будет навечно заблокирован
#

"""
this construction is equal to yield from

def delegator(gen):
    while True:
        try:
            data = yield
            gen.send(data)
        except StopIteration as e:
            g.throw(e)
"""
