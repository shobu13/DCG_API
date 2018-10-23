from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=30)
    latitude = models.FloatField()
    longitude = models.FloatField()
