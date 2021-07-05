from django.contrib import admin
from .models import Post, Comment
from users.models import Profile
from sockets.models import Channel, Message
from notifications.models import Notification


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Channel)
admin.site.register(Message)
admin.site.register(Notification)


