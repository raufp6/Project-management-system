# notifications_hq/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import Notifications
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        requested_user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'notification_%s' % self.room_name
        print(requested_user)
        print(self.room_name)
        print(self.room_group_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        print("TESTING CONNECTION AND REDIS")
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        message = json.loads(event['message'])
        command = ['command']

        # Send message to WebSocket
        # await self.send(text_data=json.dumps(message))
        await self.send(text_data=json.dumps({

            'command': command,

            'data': message,

        }))