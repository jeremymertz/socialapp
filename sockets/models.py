from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Channel(models.Model):
    channel_name = models.CharField(max_length=128, unique=True)
    User1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    User2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")
    last_message = models.CharField(max_length=1280, null=True)
    last_message_author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    connected_users = models.ManyToManyField(User, related_name='Connected_users', symmetrical=False, blank=True)
    last_message_date = models.DateTimeField(timezone.now, default=None, null=True)
    read = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.User1.username} x {self.User2.username}'


class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1280)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.author}\'s message in {self.channel}'
