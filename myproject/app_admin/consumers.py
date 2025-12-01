import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Chỉ cho phép staff users kết nối
        if self.scope["user"].is_anonymous or not self.scope["user"].is_staff:
            await self.close()
            return
        
        self.group_name = 'admin_notifications'
        
        # Tham gia vào group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Rời khỏi group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        
        # Gửi lại cho tất cả clients trong group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'notification_message',
                'message': message
            }
        )

    async def notification_message(self, event):
        # Gửi message đến WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message,
            'type': 'notification'
        }))
    
    async def rental_notification(self, event):
        # Gửi thông báo đơn thuê mới
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message,
            'type': 'rental_notification'
        }))