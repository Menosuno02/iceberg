from django.contrib.auth.models import User
from django.db import models

""" Evento """
class Event(models.Model):
    title = models.CharField(max_length=600)
    description = models.TextField(max_length=300)
    date = models.DateTimeField()
    registered_users = models.ManyToManyField(
        User, related_name='registered_events', blank=True, null=True)

    def __str__(self):
        return self.title
