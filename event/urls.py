from django.urls import path

from event.views import RegisterEvent, ShowEvents, UnregisterEvent

urlpatterns = [
    path('', ShowEvents, name='events'),
    path('events/register/<int:event_id>/',
        RegisterEvent, name='register-to-event'),
    path('events/unregister/<int:event_id>/',
        UnregisterEvent, name='unregister-from-event'),
]
