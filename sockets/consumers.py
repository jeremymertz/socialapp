import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Channel, Message
from wall.models import User
from django.shortcuts import redirect
from django.utils import timezone



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]
        self.id_1, self.id_2 = self.room_name.split('y')

        user1, user2 = await self.get_users(self.id_1, self.id_2)
        if self.user.username == user1:
            self.second_user = user2
        else:
            self.second_user = user1

        await self.add_to_connected()

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.add_to_disconnected()

    @database_sync_to_async
    def get_users(self, id1, id2):
        user1 = User.objects.get(pk=id1).username
        user2 = User.objects.get(pk=id2).username
        return user1, user2

    @database_sync_to_async
    def add_to_connected(self):
        current_channel = Channel.objects.get(channel_name=self.room_name)
        current_channel.connected_users.add(self.user)

    @database_sync_to_async
    def add_to_disconnected(self):
        current_channel = Channel.objects.get(channel_name=self.room_name)
        current_channel.connected_users.remove(self.user)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        timestamp, avatar = await self.save_message(message)


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'timestamp': timestamp,
                'avatar': avatar
            }
        )

    @database_sync_to_async
    def save_message(self, message):
        channel = Channel.objects.get(channel_name=self.room_name)
        if self.second_user in channel.connected_users.all():
            msg = Message.objects.create(channel=channel, author=self.user, content=message)
        else:
            msg = Message.objects.create(channel=channel, author=self.user, content=message, read=False)
            channel.read = False
        channel.last_message = message
        channel.last_message_author = self.user
        channel.last_message_date = timezone.now()
        timestamp = channel.last_message_date.strftime('%B %d, %Y, %H:%M.')
        channel.save()
        avatar = self.user.profile.profile_picture.url
        return timestamp, avatar

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        timestamp = event['timestamp']
        avatar = event['avatar']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'timestamp': timestamp,
            'avatar': avatar
        }))