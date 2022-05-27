from threading import Thread
import socket
from time import sleep

from classes import Target
from funcs import target_init, process

targets = []


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 5000))
        s.listen()
        while 1:
            sleep(0.0001)
            conn, addr = s.accept()
            if conn:
                thread = Thread(target=process, args=(conn, targets), daemon=True)
                thread.start()


if __name__ == '__main__':
    targets = target_init(Target)
    main()
