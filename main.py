from aiohttp import web
from asyncio import Lock
import logging

from classes import Target
from funcs import target_init, give_lowest_load_target as gllt

app = web.Application()
# routes = web.RouteTableDef()

url = '/api'
targets = []
last_task_num = None
lock = Lock()

# def copy_request(request):


# Маршрут для распределения задач
# @routes.get(f'{url}/task/')
async def send_task(request):
    async with lock:
        global last_task_num
        last_task_num = last_task_num+1 if last_task_num is not None else 0
        task_number = last_task_num
    status = None
    text = None
    headers = None
    while status != 200:
        target = await gllt(targets)
        if target is None:
            return web.Response(text='Все сервисы не доступны', status=503)
        try:
            json = await request.json()
        except:
            json = {}
        status, headers, text, json = \
            await target.send_task(task_number, request.method, request.headers, json, request.cookies)
    if json:
        return web.json_response(status=status, headers=headers, content_type=None, data=json)
    else:
        return web.json_response(text=text, status=status, headers=headers, content_type=None)

app.add_routes([web.get(f'{url}/task/', send_task),
                web.post(f'{url}/task/', send_task),
                web.put(f'{url}/task/', send_task),
                web.delete(f'{url}/task/', send_task),
                web.patch(f'{url}/task/', send_task)])

if __name__ == '__main__':
    targets = target_init(Target)
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, host='localhost', port=5000)
