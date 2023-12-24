"""
ASGI config for pms project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pms.settings')
django.setup()

from channels.auth import AuthMiddleware,AuthMiddlewareStack

from task.routing import websocket_urlpatterns
from notification.routing import websocket_urlpatterns as notification_urls


application = ProtocolTypeRouter({
    "http":get_asgi_application(),
    "websocket":AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns+
            notification_urls
        )
    )
})
