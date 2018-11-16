from django.db import models
from user.models import User


class Event(models.Model):
    name = models.CharField(max_length=30)
    place = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_owner')
    participant = models.ManyToManyField(User)

    def __str__(self):
        return self.name
