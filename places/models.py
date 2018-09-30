from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=30)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
