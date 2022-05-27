from datetime import datetime
from time import sleep
from threading import Thread
import socket

from config import BALANCER_URL, URLS


def send(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send('task'.encode())
        while 1:
            sleep(0.001)
            try:
                request = s.recv(4096)
            except OSError:
                continue
            if request:
                s.close()
                print(request.decode())


# Функция - спамер
def main():
    host, port = BALANCER_URL.split(':')
    while 1:
        thread = Thread(target=send, args=(host, int(port)), daemon=True)
        thread.start()
        sleep(0.1)


def send_order(command):
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host, port = URLS[0].split(':')
    sc.connect((host, int(port)))
    sc.send(command.encode())
    while 1:
        sleep(0.001)
        request = sc.recv(4096)
        if request:
            sc.close()
            print(request)
            break


# Запускается в отдельном потоке, чтобы имитировать отключение одного из клиентов
def target_switch():
    sleep(100)
    send_order('shutdown')
    sleep(100)
    send_order('startup')


if __name__ == '__main__':
    thread = Thread(target=target_switch, daemon=True)
    thread.start()
    main()
