from celery import shared_task

from .import_yaml import Command


@shared_task(name="Импорт товаров")
def etl_task(*args, **kwargs):
    func = Command().handle()
    print(func)
    if func:
        unloads = func.load()
        multiplication = func.transform(unloads)
        func.extract(multiplication)

    return "my result data"
