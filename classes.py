import aiohttp
from requests import get


class Target:

    def __init__(self, url=None, name=None):
        self.available = False
        self.url = url
        self.tasks_num = 0
        self.name = name
        self.tasks_in_work = []

    def __repr__(self):
        return self.name

    def is_available(self):
        url = f'{self.url}is_alive/'
        self.available = get(url).json()
        return self.available

    def __add_task(self, task):
        self.tasks_num += 1
        self.tasks_in_work.append(task)

    def __sub_task(self, task):
        self.tasks_num -= 1
        self.tasks_in_work.remove(task)

    async def send_task(self, task_num):
        task = f'task_{task_num}'
        self.__add_task(task)
        url = f'{self.url}task/{task_num}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as resp:
                text, status = await resp.text(), resp.status
        self.__sub_task(task)
        return status, text

    def start_up(self):
        response = get(url=f'{self.url}start/')
        return response

    def shutdown(self):
        response = get(url=f'{self.url}stop/')
        return response