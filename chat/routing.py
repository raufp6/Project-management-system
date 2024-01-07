from django.urls import re_path,path
from . import consumers

websocket_urlpatterns = [
    re_path(
		r'ws/chat/(?P<userId>\w+)/chat/$',
		consumers.ChatConsumer.as_asgi()
	),
]
