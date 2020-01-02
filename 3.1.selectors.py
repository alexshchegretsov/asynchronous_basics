# -*- coding: utf-8 -*-
import socket
import selectors

# модуль selectors - кроссплатформенная обёртка над функцией select
# создаём selector для текущей ОС
selector = selectors.DefaultSelector()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 5000))
    server_socket.listen()
    # как только создастся серверный сокет - зарегистрируем его в селекторе
    # который будет следить за входящими соединениями
    # если соединение поступило - передаём серверный сокет в функцию accept_connection
    # где создастся клиентский сокет, который будет обслуживать поступившее соединение
    # селектор начнёт мониторить клиентский сокет на чтение
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print("connection from ", addr)
    # как только мы напишем что-нибудь в сокет - сработает селектор на событие "чтение"
    # и передаст клиентский сокет в функцию send_message
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)

def send_message(client_socket):
    request = client_socket.recv(4096)
    if request:
        client_socket.sendall(b"Hello man\n")
    else:
        # если закрываем соединение - перестаём мониторить клиентский сокет
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    while True:
        # select() возвращает кортеж (key, events) - нам нужен только key
        events = selector.select()

        # первый элемент - key - это объект SelectorKey
        # который является NamedTuple
        # он связывает сокет, ожидаемое событие и функцию, которую нужно вызвать по наступлению этого события
        # у объекта SelectorKey - те же поля, что мы заполняли при регистрации
        # fileobj, events, data


        for key, _ in events:
            # достаём параметр data из селектора, т.е. функцию
            callback = key.data
            # передаём в функцию параметр fileobj - client/server socket
            callback(key.fileobj)

if __name__ == '__main__':
    server()
    event_loop()
