from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from event.models import Event

""" Eventos """
@login_required
def ShowEvents(request):
    context = {
        'events': Event.objects.prefetch_related('registered_users'),
        'user': request.user,
    }
    return render(request, 'event/all_events.html', context)


@login_required
def RegisterEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    user = request.user
    if user not in event.registered_users.all():
        event.registered_users.add(user)
    return redirect('events')


@login_required
def UnregisterEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    user = request.user
    if user in event.registered_users.all():
        event.registered_users.remove(user)
    return redirect('events')
