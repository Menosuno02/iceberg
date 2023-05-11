from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from notification.views import ShowNotifications

urlpatterns = [
    path('', ShowNotifications, name='show-notifications'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)