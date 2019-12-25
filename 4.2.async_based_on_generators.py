import socket
from select import select

# мы преобразовали наши функции в генераторы, которые отдают кортежи
# где первый элемент - фильтрующий признак, по которому мы определяем
# куда пойдёт сокет, находящийся во втором элементе кортежа
# т.е. в какой список на мониторинг он пойдёт: на готовность к чтению или записи.
#
# 1. добваляем генератор server() в задачи
# 2. в event_loop() поскольку есть задача, мы получаем read, server_socket = next(task)
# в server()[т.е. task] мы вышли на первом yield и ждём следующего next
# 3. добавляем в словарь на мониторинг to_read[sock] = task[ждёт следующий next]
# 4. задачи закончились - переходим во внутренний while[пока что мониторим серверный сокет на чтение]
# 5. как только мы попытались установить соединение - отрабатывает selector,
# добавляющий в задачи генератор, ждущий следующего next() tasks.append(to_read.pop(sock))
# 6. выходим из внутреннего while, поскольку появилась новая задача
# 7. делаем второй read, server_socket = next(task)
# 7.1 принимаем соединение и создаём клиентский сокет: client_socket, addr = server_socket.accept()
# 7.2 добавляем клиентский генератор в задачи: tasks.append(client(client_socket))
# 7.3 опять добавляем server_socket в словарь на мониторинг to_read[sock] = task[ждёт следующий next]
# 8. первая задача закончилась - переходим ко второй - обработка генератора client(client_socket)
# 8.1. read, client_socket = next(task2)
# 8.2. добавляем в мониторинг на чтение to_read[sock] = task2[ждёт следующего next]
# 8.3. задачи закончились - входим во внутренний цикл - мониторим два сокета на чтение
# 9. отправляем сообщение со стороны клиента
# 10. отрабатывает selector и добавляет генератор client() в задачи tasks
# 11. выходим из внутреннего while
# 12. write, client_socket = next(task2) - теперь уже на запись
# 13. добавляем в мониторинг на запись to_write[sock] = task2
# 13. поскольку буфер свободен то сразу работает selector и отдаст генератор в задачи
# 14. отправляем сообщение,
# 15. смещаемся до следующего yield и опять добавляем клиентский сокет в мониторинг на чтение

tasks, to_read, to_write = [], {}, {}
"""
to_read = {
    server_socket: server(),
    client_socket: client(client_socket)
    }
"""


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 5000))
    server_socket.listen()
    while True:
        # read
        yield ("read", server_socket)
        client_socket, addr = server_socket.accept()
        # добавляем генератор в задачи
        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        # read
        yield ("read", client_socket)
        request = client_socket.recv(4096)

        print(request)
        if not request:
            break

        # write
        yield ("write", client_socket)
        client_socket.sendall(b"hi there\n")

    client_socket.close()


def event_loop():
    while any([tasks, to_read, to_write]):

        while not tasks:
            # как только отлавливается событие -
            # извлекаем из словаря соответствующую пару сокет-генератор,
            # и генератор передаём в список tasks
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])
            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))
            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        # получение генератора из списка tasks
        # и вызов next() у генератора task, который отдаёт нам кортеж с фильтром и сокетом
        try:
            task = tasks.pop(0)
            reason, sock = next(task)
            if reason == "read":
                to_read[sock] = task
            if reason == "write":
                to_write[sock] = task
        except StopIteration:
            print("Done")


if __name__ == '__main__':
    tasks.append(server())
    event_loop()
