from django.contrib import admin

from .models import Profile, Interest, Relationship

admin.site.register(Profile)
admin.site.register(Interest)
admin.site.register(Relationship)