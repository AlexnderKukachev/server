import socket
import time


class Target:

    def __init__(self, host: str = None, port: int = None, name=None):
        self.host = host,
        self.port = port,
        self.tasks_num = 0
        self.tasks = []
        self.name = name

    def __repr__(self):
        return self.name

    def __del__(self):
        self.sc.close()

    # def available(self):
    #     sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     sc.connect((self.host[0], self.port[0]))
    #     sc.send('ping')
    #     sc.close()
    #     with

    def __add_task(self, data):
        self.tasks_num += 1
        self.tasks.append(data)

    def sub_task(self, data):
        self.tasks_num -= 1
        self.tasks.remove(data)

    def try_connect(self):
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.connect((self.host[0], self.port[0]))
        sc.send('ping'.encode())
        import time
        while 1:
            time.sleep(0.001)
            request = sc.recv(4096).decode()
            print(request)
            if request == 'pong':
                sc.close()
                return True
            elif request == 'Unavailable':
                sc.close()
                return False

    def send_task(self, data):
        self.__add_task(data)
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.connect((self.host[0], self.port[0]))
        sc.send(data)
        while 1:
            time.sleep(0.001)
            request = sc.recv(4096)
            if request:
                print(request)
                sc.close()
                self.sub_task(data)
                return request

    def startup(self):
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.connect((self.host[0], self.port[0]))
        sc.send('startup'.encode())
        while 1:
            time.sleep(0.001)
            request = sc.recv(4096)
            if request:
                sc.close()
                return request

    def shutdown(self):
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc.connect((self.host[0], self.port[0]))
        sc.send('shutdown'.encode())
        while 1:
            time.sleep(0.001)
            request = sc.recv(4096)
            if request:
                sc.close()
                return request
