# -*- coding: utf-8 -*-
import socket
from select import select

# цель
# пока происходит ожидание ввода-вывода данных(чтение-запись из/в буфер сокета) -
# то нам нужно как-то передать управление, той части кода, которая уже готова для этих операций
# т.е. пока один сокет ждёт - мы передаём управление другому сокету и вызываем соответствующие методы
# исходя из этого возникает две задачи:
# 1. определить какие сокеты готовы для чтения/записи (вызвать методы)
# 2. описать механизм переключения

# для реализации event_loop нам нужно предусмотреть некий "механизм"
# который в определённый момент времени вызывал бы функции accept_connection() и send_message()
# и передавал бы в них нужные сокеты

# если говорить о серверном сокете, а конкретно о методе .accept(),
# то мы должны дождаться пока во входящем буфере появятся данные о новом подключении
# тоже самое относится и к клиентскому сокету с методом .recv()
# т.е. событием будет появление во входящем буфере клиентского сокета данных от пользователя
# для метода sendall() ситуация наоборот - он не читает из буфера, но он пишет в буфер отправки
# и здесь событием будет очистка буфера отправки и соответственно
# готовность сокета туда что-то записывать

# select - это системная функция, которая нужна для мониторинга изменений
# состояний файловых объектов и сокетов
# в unix одна из ключевых идей - всё файл - все устройства, USB, клавиатура, системный календарь
# с точки зрения ОС - это всё файлы, каждый запущенный процесс - это тоже файл
# когда мы у серверного сокета вызываем метод .bind() - создаётся файл сокета
# так вот select работает с любым объектом, который поддерживает метод .fileno()
# этот метод возвращает файловый дескриптор
# файловый дескриптор - это просто номер файла, целое число,
# которое ассоциируется с конкретным файлом в системе

# допустим у нас есть два файла x.py, y.py - в системе они зарегистрированы под номерами 9245 и 9999
# и если мы хотим записать что-то в x.py, то ОС запишет в файл под номером 9245,
# т.к. она знает что имя x.py зарегистрировано на номер 9245, x.py как бы ссылается на 9245
# так вот 9245 и 9999 это и есть файловые дескрипторы

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 5000))
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.listen()

# инициализируем список объектов на чтение, за которыми будет следить select
to_monitor = []

# как только мы установили соединение с сервером - тут же срабатывает select
# создаётся client_socket и добавляется в to_monitor
def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print("connection from: ", addr)
    to_monitor.append(client_socket)

# как только мы отправили что-то в клиентский сокет - срабатывает select
# идентифицируем клиенткий сокет - вызываем send_message()
def send_message(client_socket):
    request = client_socket.recv(4096)
    if request:
        client_socket.sendall(b"Hello from inner loop\n")
    else:
        client_socket.close()


def event_loop():
    while True:
        # у нас есть список с сокетами, которые нужно мониторить
        # на предмет доступности на чтение,
        # т.е. когда у них во входящих буферах появляются какие-то данные
        # read, write, exceptions
        print("to monitor is: ", to_monitor)
        ready_to_read, _, _ = select(to_monitor, [], [])
        print("READY LENGTH IS:", len(ready_to_read))
        print("ready is: ", ready_to_read)

        for sock in ready_to_read:
            if sock is server_socket:
                # теперь клиентский сокет нужно добавить в to_monitor
                print("SERVER SOCKET")
                accept_connection(sock)
            else:
                print("CLIENT SOCKET")
                send_message(sock)


"""
select(...)
        select(rlist, wlist, xlist[, timeout]) -> (rlist, wlist, xlist)

        Wait until one or more file descriptors are ready for some kind of I/O.
        The first three arguments are sequences of file descriptors to be waited for:
        rlist -- wait until ready for reading
        wlist -- wait until ready for writing
        xlist -- wait for an ``exceptional condition''
        If only one kind of condition is required, pass [] for the other lists.
        A file descriptor is either a socket or file object, or a small integer
        gotten from a fileno() method call on one of those.

        The optional 4th argument specifies a timeout in seconds; it may be
        a floating point number to specify fractions of seconds.  If it is absent
        or None, the call will never time out.

        The return value is a tuple of three lists corresponding to the first three
        arguments; each contains the subset of the corresponding file descriptors
        that are ready.
"""

if __name__ == '__main__':
    to_monitor.append(server_socket)
    event_loop()
