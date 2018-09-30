from django.db import models

from user.models import User


class Promo(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    validation = models.BooleanField()
