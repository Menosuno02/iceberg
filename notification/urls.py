from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from notification.views import ShowNotifications

urlpatterns = [
    path('', ShowNotifications, name='show-notifications'),
]
