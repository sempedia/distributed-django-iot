import os
from celery import Celery

# import queu and exchnage from kombu so we can declare celery tasks
# in a list and use them 
from kombu import Queue, Exchange


# set the default os env variable for  the module itself: core.settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


# we declare the app which will be based on the module 'core' as well
app = Celery('core')

# we get our related configuration from 'django.conf:settings'
app.config_from_object('django.conf:settings', namespace='CELERY')

# set autodiscoveryng tasks so celery is working 
app.autodiscover_tasks()

# Declare the nodes we will use for our tasks
nodes = ['node-1', 'node-2', 'node-3', 'node-4']

# Declare the celery tasks queues into a list:
# CELERY_TASK_QUEUES = [
    # declare a the queues we will use / hardcoded in a list
    # [Queue('node-1', Exchange('node-1'), routing_key='node-1'),
    # Queue('node-2', Exchange('node-2'), routing_key='node-2'),
    # Queue('node-3', Exchange('node-3'), routing_key='node-3'),
    # Queue('node-4', Exchange('node-4'), routing_key='node-4'),]
    

# Iterating through all the nodes and append them to our empty
# CELERY_TASK_QUEUES to not be hardcoed by us in the list
# then also append the scheduler for our task

CELERY_TASK_QUEUES = []
CELERY_BEAT_SCHEDULE = {}
for node in nodes:
    CELERY_TASK_QUEUES.append(
        Queue(node, Exchange(node), routing_key=node)
        )
    key = f'check_temp_{node}'
    CELERY_BEAT_SCHEDULE[key] = {
        'task': 'sensors.tasks.measure_temp_task',
        'schedule': 5.0, # every 5  seconds that task will run
        'options': { 'queue': node} # you can trigger this option manually by doing command:
        # measure_temp_task.apply_async(queue='node-1')
    }

app.conf.task_queues = CELERY_TASK_QUEUES
# we set our app beat_schedule to be equal with 
# the dictionary created earlier
# command to check this schedule is working is:
# celery -A core beat -l info
# we can also run the beat schedule from our database we created into settings.py file 
# in the same time.
app.conf.beat_schedule = CELERY_BEAT_SCHEDULE

# Define a celery beat schedule dictionary hardcoded that we will fill out 
# with tasks that also have different parameters included
# 1. declare the task itself that we created in the tasks.py file
# 2. declare our schedule for the task - by default we can give it a value of seconds
# depends on how often you need the temperature/data  to be tracked.
# CELERY_BEAT_SCHEDULE = {
    # 'check_temp': {
        # 'task': 'sensors.tasks.measure_temp_task',
        # 'schedule': 5.0, # every 5  seconds that task will run
        # 'options': { 'queue': 'node-2'} # you can trigger this option manually by doing command:
        # # measure_temp_task.apply_async(queue='node-1')}
        


