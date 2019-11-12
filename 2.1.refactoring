# -*- coding: utf-8 -*-
import socket

# ни о какой асинхронной обработке сокетов здесь речи быть не может
# поскольку этот скрипт с самого начала спроектирован как синхронный:
# 1. создаём серверный сокет
# 2. передаём серверный сокет в функцию accept_connection, где создаётся клиентский сокет
# 3. передаём клиентский сокет в функцию send_message()
# т.е. выполняются действия одно за другим и
# для того чтобы превратить этот код в асинхронный
# его нужно определённым образом переделать,
# причём переделать так, что бы все эти две функции accept_connection() и send_message()
# стали как-бы независимыми, их нужно упростить,
# чтобы любую из них можно было в любом порядке вызвать тогда, когда мы этого захотим
# т.е. нам нужно уменьшить их связность
# 1. из accept_connection() убрать вызов send_message(),
# 2. убрать циклы,
# 3. создать event_loop,
# 4. использовать select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 5000))
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.listen()

def accept_connection(server_socket):
    while True:
        client_socket, addr = server_socket.accept()
        print("connection from: ", addr)
        send_message(client_socket)


def send_message(client_socket):
    while True:
        request= client_socket.recv(4096)

        if not request:
            break
        else:
            client_socket.sendall(b"Hello from inner loop\n")
    client_socket.close()

if __name__ == '__main__':
    accept_connection(server_socket)