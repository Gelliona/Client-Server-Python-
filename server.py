import socket
import threading

new_socket = socket.socket()
new_socket.bind(('', 55555))
new_socket.listen()

print("Сервер запущен")

clients = []
nicknames = []


def connect(client, addr):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            print("Соединение с {} разорвано".format(str(addr)))
            broadcast('{} покинул чат!'.format(nickname).encode())
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, addr = new_socket.accept()
        print("Соединение с {} установлено".format(str(addr)))

        client.send('Авторизация'.encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)

        """print("Ник: {}".format(nickname))"""
        broadcast("{} присоединился к чату!".format(nickname).encode())
        client.send('Соединение с сервером установлено!'.encode())

        thread = threading.Thread(target=connect, args=(client, addr))
        thread.start()


def broadcast(mes):
    for client in clients:
        client.send(mes)


receive()
