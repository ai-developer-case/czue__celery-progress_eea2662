from celery import Celery

from celery_progress.backend import Progress, WEBSOCKETS_AVAILABLE
from celery_progress.websockets.backend import push_update


class CeleryProgressMiddleware:

    def __init__(self, app: Celery):
        self.app = app

    def __call__(self, task_func):
        def wrapper(*args, **kwargs):
            task_id = kwargs.get(self.app.task_always_eager) \
                or args[0].request.id \
                or kwargs.get('request', {}).get('id')
            result = task_func(*args, **kwargs)
            if WEBSOCKETS_AVAILABLE:
                push_update(task_id)
            return result
        return wrapper