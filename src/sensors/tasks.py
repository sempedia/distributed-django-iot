# import helpers for using our main configuration
import helpers

# import the decorator shared_task
from celery import shared_task

# import our apps from django.apps
from django.apps import apps


# import timezone to can add the time to our tasks
from django.utils import timezone

# import the collect package we just defined into sensors/collect.py
from . import collect 

# option 1: import the Metric model from .models 
# from .models import Metric

# we use the @shared_task decorator and define a mesure_temp_task() function
# to mesure our temperature

@shared_task
def measure_temp_task():
    # by default we will make the temperature as collect.get_random_temp()
    temp = collect.get_random_temp()
    
    # where do we store this temperature we collect ????
    # how we are store the temperature into our database??? 
    # one option is: from .models import Metric to bring in the model class itself.add()
    # option 2: we can use this task inside of our model class and 
    # import the model into the task 
    # we add our model here as Metric and this will be 
    # apps.get_model('sensors', 'Metric') where 
    # 'sensors' is our app we work on  now and 'Metric' is the model itself 
    # from our 'sensor' app.
    Metric = apps.get_model('sensors', 'Metric')
    
    # add the node id from our main configuration 
    # as an env variable NODE_ID and for this we need to import helpers
    # the default of the node id will be '0'
    # each instance that will running celery will be on a different 
    # node and will have a different node id for different machines that will run this celery
    # version 
    node_id = helpers.config('NODE_ID', default=0)
    
    # create the task 
    Metric.objects.create(
        node_id=node_id,
        temperature=temp,
        time=timezone.now()
        
    )
    
    
    
    