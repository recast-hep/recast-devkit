from celery import Celery
app = Celery('localapp')
app.config_from_object('recastdevkit.devbackend.localconfig')