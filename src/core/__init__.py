# we import the app as celery_app from .celery.py file 
from .celery import app as celery_app 


# we set this app to __all__ to can use all from our celery_app
__all__ = [
    'celery_app'
]