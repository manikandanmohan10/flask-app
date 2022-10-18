from src.blueprint.bp import AuthBlueprint, QuoteBlueprint
from celery import Celery
from run import app

# def get_celery():
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


blueprints = []
blueprints.append(AuthBlueprint())
blueprints.append(QuoteBlueprint())

for apis in blueprints:
    app.register_blueprint(apis)