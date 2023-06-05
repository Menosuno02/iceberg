from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from event.models import Event


@login_required
def ShowEvents(request):
    context = {
        'events': Event.objects.all(),
        'user': request.user
    }
    return render(request, 'event/all_events.html', context)


def RegisterEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    user = request.user
    if user not in event.registered_users.all():
        event.registered_users.add(user)
    return redirect('events')
