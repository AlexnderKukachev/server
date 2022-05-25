import aiohttp
import asyncio
from datetime import datetime
from time import sleep
from threading import Thread
from requests import get

from config import BALANCER_URL, URLS

task_num = 0


# Функция - спамер
async def main():
    global task_num
    async with aiohttp.ClientSession() as session:
        async with session.get(BALANCER_URL) as resp:
            print(datetime.now(), f'task_{task_num} started')
            text, status = await resp.text(), resp.status
            print(datetime.now(), f'task_{task_num} complete\n'
                                  f'message: {text}, status: {status}')
    sleep(0.2)
    task_num += 1


# Запускается в отдельном потоке, чтобы имитировать отключение одного из клиентов
def target_switch():
    sleep(10)
    response = get(f'{URLS[0]}stop/')
    print(response.text)
    sleep(10)
    response = get(f'{URLS[0]}start/')
    print(response.text)


if __name__ == '__main__':
    thread = Thread(target=target_switch, daemon=True)
    thread.start()
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(main()) for _ in range(1000)]
    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)
