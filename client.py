import socket
import threading

my_socket = socket.socket()
my_socket.connect(('127.0.0.1', 55555))

my_name = input("Выберите ник: ")


def send_mess():
    while True:
        message = '{}: {}'.format(my_name, input(''))
        my_socket.send(message.encode())


def get_mess():
    while True:
        try:
            message = my_socket.recv(1024).decode()
            if message == 'Авторизация':
                my_socket.send(my_name.encode())
            else:
                print(message)
        except:
            print("Ошибка!")
            my_socket.close()
            break


send_thread = threading.Thread(target=send_mess)
get_thread = threading.Thread(target=get_mess)
send_thread.start()
get_thread.start()

