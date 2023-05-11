from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from notification.models import Notification

""" Ver notificaciones """
@login_required
def ShowNotifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')
    return render(request, 'blog/notifications.html', {'notifications':notifications,})