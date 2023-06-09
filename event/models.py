from django.contrib.auth.models import User
from django.db import models

""" Evento """
class Event(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=600)
    location = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField()
    registered_users = models.ManyToManyField(
        User, related_name='registered_events', blank=True, null=True)
    image = models.ImageField(default='default-placeholder.png',
                                upload_to='fotos_evento_folder', blank=True, null=True, max_length=200)

    def __str__(self):
        return self.title
