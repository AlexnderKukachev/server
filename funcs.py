from config import URLS


def target_init(Target):
    targets = []
    count = 0
    for url in URLS:
        ip, port = url.split(':')
        target = Target(ip, int(port), f'target_{count}')
        targets.append(target)
        count += 1
    return targets


def process(conn, targets):
    request = conn.recv(4096)
    if request:
        target = give_lowest_load_target(targets)
        print(target)
        if target:
            conn.send(target.send_task(request))
        else:
            conn.send('Все сервисы не доступны'.encode())
    conn.close()


def give_lowest_load_target(targets):
    lowest_tasks_num = None
    rem_target = None
    for target in targets:
        try:
            available = target.try_connect()
        except ConnectionRefusedError:
            continue
        if not available:
            continue
        if lowest_tasks_num is None:
            lowest_tasks_num = target.tasks_num
            rem_target = target
        elif lowest_tasks_num > target.tasks_num:
            lowest_tasks_num = target.tasks_num
            rem_target = target
    return rem_target



