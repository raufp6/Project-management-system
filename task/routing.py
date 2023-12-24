from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    # path('ws/notifications/', consumers.TaskNotificationConsumer.as_asgi()),
    re_path(r'ws/notificationss/(?P<room_name>\w+)/$', consumers.TaskNotificationConsumer.as_asgi()),
    # re_path(r'ws/notifications/', consumers.TaskNotificationConsumer.as_asgi()),
    

]