from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=30)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
