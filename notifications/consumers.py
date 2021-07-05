import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import time
from wall.models import Post, Comment
from sockets.models import Channel
from django.contrib.auth.models import User


class Notifications(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            self.group_name = self.scope['url_route']['kwargs']['username']

        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )


    @database_sync_to_async
    def get_sender_info(self, sender_username):
        sender = User.objects.get(username=sender_username)
        sender_profile = sender.profile.get_absolute_url()
        sender_avatar = sender.profile.profile_picture.url
        return sender_profile, sender_avatar

    @database_sync_to_async
    def get_post_info(self, post_number):
        post = Post.objects.get(id=post_number)
        post_picture = post.picture.url
        post_url = post.get_absolute_url()
        return post_picture, post_url

    @database_sync_to_async
    def get_info_comment(self, comment_number):
        comment = Comment.objects.get(id=comment_number)
        comment_content = comment.content
        return comment_content

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        sender_username = text_data_json['liked']
        sender_profile, sender_avatar = await self.get_sender_info(sender_username)
        notification_type = ""
        if 'post-no' in text_data_json and 'comment-no' in text_data_json:
            notification_type = "notification"
            post_number = text_data_json['post-no']
            comment_number = text_data_json['comment-no']
            post_picture, post_url = await self.get_post_info(post_number)
            comment_content = await self.get_info_comment(comment_number)
            channel = None
            if len(comment_content) > 20:
                message = f'commented: {comment_content[0:20]}...'
            else:
                message = f'commented: {comment_content}'
        elif 'post-no' in text_data_json:
            notification_type = "notification"
            post_number = text_data_json['post-no']
            post_picture, post_url = await self.get_post_info(post_number)
            message = f'liked your post.'
            channel = None
        elif text_data_json['channel']:
            channel = text_data_json['channel']
            notification_type = "private_message"
            post_picture = None
            post_url = None
            message = text_data_json['message']
        else:
            notification_type = "notification"
            post_picture = None
            post_url = None
            channel = None
            message = f'followed you.'

        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'post_url': post_url,
                'sender_username': sender_username,
                'sender_profile': sender_profile,
                'sender_avatar': sender_avatar,
                'post_picture': post_picture,
                'notification_type': notification_type,
                'channel': channel,
            }
        )
        await self.close()

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        post_url = event['post_url']
        sender_profile = event['sender_profile']
        sender_username = event['sender_username']
        sender_avatar = event['sender_avatar']
        post_picture = event['post_picture']
        notification_type = event['notification_type']
        channel = event['channel']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'post_url': post_url,
            'sender_username': sender_username,
            'sender_profile': sender_profile,
            'sender_avatar': sender_avatar,
            'post_picture': post_picture,
            'notification_type': notification_type,
            'channel': channel,
        }))