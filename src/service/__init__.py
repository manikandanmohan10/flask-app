from celery import Celery
import src


# def get_celery():
#     app = src.create_app()    
#     celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
#     celery.conf.update(app.config)

#     return celery