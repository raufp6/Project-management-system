from django.urls import path,re_path
from . import consumers

websocket_urlpatterns = [
    # path('ws/notifications/all/', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/notifications/(?P<room_name>\w+)/$', consumers.NotificationConsumer.as_asgi()),

]
