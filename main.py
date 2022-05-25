from aiohttp import web
from asyncio import Lock
import logging

from classes import Target
from funcs import target_init, give_lowest_load_target as gllt

app = web.Application()
routes = web.RouteTableDef()

url = '/api'
targets = []
last_task_num = None
lock = Lock()


# Маршрут для распределения задач
@routes.get(f'{url}/task/')
async def send_task(request):
    async with lock:
        global last_task_num
        last_task_num = last_task_num+1 if last_task_num is not None else 0
        task_number = last_task_num
    code = None
    task = None
    while code != 200:
        target = await gllt(targets)
        if target is None:
            return web.Response(text='Все сервисы не доступны', status=503)
        code, task = await target.send_task(task_number)
    return web.Response(text=task, status=code)

app.add_routes(routes)

if __name__ == '__main__':
    targets = target_init(Target)
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, host='localhost', port=5000)
