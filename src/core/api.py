# import List from typing so our data to be an actual list of data
from typing import List

# import datetime for our time_group field
from datetime import datetime

# import the NinjaAPi library
# import Schema from ninja so we can alter the 
# response we get back from our REST API call
# and transfrom it in JSON data instead of 
# the queryset we receive from our database directly
# that our rest api cannot handle unserialized.add()
from ninja import NinjaAPI, Schema

# import the services from sensors and 
# the Metric from sensors.models for using them 
# when we want to serialize the data coming from db 
# and then json-ify it and display it on our api:
# http://localhost:8000/api/temps
from sensors import services
from sensors.models import Metric


# create/initialize the api service:
api = NinjaAPI()


# we define a new Schema so we can alter the response coming from 
# our api service and serialize it into JSON format so we can see it 
# displayed on http://localhost:8000/api/temps
class AvgTempSchema(Schema): # pydantic model version of a schema (like a typescript model) 
    # we define the data fileds that is coming from our database
    # and add it's type
    avg_temp: float
    time_group: datetime

# add the GET request decorator above our function that will get the everage temperature.
# as response of our request we will get our AvgTempSchema object 
# where we have validate our database fields that are coming in.
# we declare the datatype beeing a list of the avg tem schema so 
# we can have all the list of data from our database serialized 
# and displaied on to the rest api endpoint
@api.get('/temps', response=List[AvgTempSchema])
# define a function to get average temperature values
# the function will take the request and will return back 
# the values that we want : {"hello": "world"} for starting 
def get_average_temps(request):
    qs = services.get_avg_temp()
    # ninja will get our queryset and turn it automatically into this schema we created:
    # AvgTempSchema
    return qs

# we get displayed a list of our avg recent temperature metrics 
# in a range of minutes:

# [
#     {
#         "avg_temp":61.88888840404956754,
#         "time_group": "2024-07-09T10:25:00Z"
#     },
#     {
#         "avg_temp":60.8883546440404956754,
#         "time_group": "2024-07-09T10:25:00Z"
#     },
#     {
#         "avg_temp":58.34472849404040006748,
#         "time_group": "2024-07-09T10:25:00Z"
#     },
#     {
#         "avg_temp":64.856475839564804956754,
#         "time_group": "2024-07-09T10:25:00Z"
#     } 
# ]
    
    

# the schema for our rest api endpoint that will display the avg node temps
class NodeAvgTempSchema(Schema): 
    node_id: int
    avg_temp: float
    time_group: datetime
    
    
# rest api endpoint that display our avg node temp 
@api.get('/temps/node', response=List[NodeAvgTempSchema])
def get_average_temps(request):
    qs = services.get_node_avg_temp()
    return qs

# we get avg nodes temp as:

# [
#     {
#         " node_id": 1,
#         "avg_temp":61.88888840404956754,
#         "time_group": "2024-07-09T10:25:00Z"
#     },
#     {
#         " node_id": 2,
#         "avg_temp":60.8883546440404956754,
#         "time_group": "2024-07-09T10:25:00Z"
#     },
#     {
#         " node_id": 3,
#         "avg_temp":58.34472849404040006748,
#         "time_group": "2024-07-09T10:25:00Z"
#     },
#     {
#         " node_id": 1,
#         "avg_temp":64.856475839564804956754,
#         "time_group": "2024-07-09T10:25:00Z"
#     } 
# ]

# the schema for our rest api endpoint that will display the max-min temps
class MaxMinAvgTempSchema(Schema): 
    max_temp: float
    min_temp: float
    
    
# rest api endpoint that display our min-max temp 
# we will have a single valu of max and min temp so we don't need a List here
@api.get('/temps/maxmin', response=MaxMinAvgTempSchema)
def get_average_temps(request):
    qs = services.get_max_min_temp()
    return qs


# we get displayed a max-min temperature metric 
# in a range of minutes: http://localhost:8000/api/temps/maxmin

# [
#     {
#         "max_temp": 129.88888840404956754,
#         "min_temp": 0.01123466570404956754
#     },
 
# ]
    
    
# the schema for our rest api endpoint that will display the node max-min temps
class NodeMaxMinAvgTempSchema(Schema): 
    node_id: int
    max_temp: float
    min_temp: float
    
    
# rest api endpoint that display our node min-max temp 
@api.get('/temps/nodes/maxmin', response=List[NodeMaxMinAvgTempSchema])
def get_average_temps(request):
    qs = services.get_node_max_min_temp()
    return qs