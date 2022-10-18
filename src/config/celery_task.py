# from src.service import get_celery 
# import celery
from src.blueprint import celery

# celery = get_celery()

@celery.task()
def my_background_task():
    print('From celery')

# task = my_background_task.delay()

