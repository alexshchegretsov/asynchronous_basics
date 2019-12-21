import socket


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 5000))
    server_socket.listen()
    while True:
        # read
        client_socket, addr = server_socket.accept()
        client(client_socket)


def client(client_socket):
    while True:
        # read
        request = client_socket.recv(4096)
        print(request)
        if not request:
            break
        # write
        client_socket.sendall(b"hi there\n")
    client_socket.close()

if __name__ == '__main__':
    server()