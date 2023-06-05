"""
ASGI config for iceberg project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

import django
from channels.routing import get_default_application
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iceberg.settings')
django.setup()
application = get_default_application()
