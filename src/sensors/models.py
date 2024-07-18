from django.db import models
from timescale.db.models.models import TimescaleModel

# Create your models here.
class Metric(TimescaleModel):
    node_id = models.IntegerField(default=0)
    temperature = models.FloatField()
    