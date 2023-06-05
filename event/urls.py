from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from event.views import RegisterEvent, ShowEvents

urlpatterns = [
    path('', ShowEvents, name='events'),
    path('events/register/<int:event_id>/',
        RegisterEvent, name='register_to_event'),
]
