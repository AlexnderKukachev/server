from config import URLS


def target_init(Target):
    targets = []
    count = None
    for url in URLS:
        count = count+1 if count is not None else 0
        target = Target(url, f'target_{count}')
        targets.append(target)
        target.start_up()
    return targets


async def give_lowest_load_target(targets):
    lowest_tasks_num = None
    rem_target = None
    for target in targets:
        print(target.name)
        print(target.tasks_num)
        print(target.tasks_in_work)
        print('*******************************')
        alive = target.is_available()
        if not alive:
            continue
        elif lowest_tasks_num is None:
            lowest_tasks_num = target.tasks_num
            rem_target = target
        elif lowest_tasks_num > target.tasks_num:
            lowest_tasks_num = target.tasks_num
            rem_target = target
    return rem_target



