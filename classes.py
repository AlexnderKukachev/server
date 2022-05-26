import aiohttp
from requests import get


class Target:

    def __init__(self, ip: str = None, port: str = None, name=None):
        self.available = False
        self.ip = ip,
        self.port = port,
        self.tasks_num = 0
        self.name = name
        self.tasks_in_work = []

    def __repr__(self):
        return self.name

    def is_available(self):
        url = f'http://{self.ip[0]}:{self.port[0]}/api/is_alive/'
        self.available = get(url).json()
        return self.available

    def __add_task(self, task):
        self.tasks_num += 1
        self.tasks_in_work.append(task)

    def __sub_task(self, task):
        self.tasks_num -= 1
        self.tasks_in_work.remove(task)

    async def send_task(self, task_num, method, headers, json, cookies):
        task = f'task_{task_num}'
        self.__add_task(task)
        url = f'/api/task/{task_num}'
        async with aiohttp.ClientSession(f'http://{self.ip[0]}:{self.port[0]}') as session:
            async with session.request(method=method, url=url, headers=headers, cookies=cookies, json=json) as resp:
                status, headers, text = resp.status, resp.headers, await resp.text()
                try:
                    json = await resp.json()
                except:
                    json = {}
        self.__sub_task(task)
        return status, headers, text, json

    def start_up(self):
        response = get(url=f'http://{self.ip[0]}:{self.port[0]}/api/start/')
        return response

    def shutdown(self):
        response = get(url=f'http://{self.ip[0]}:{self.port[0]}/api/stop/')
        return response
