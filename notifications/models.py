from django.db import models
from django.contrib.auth.models import User
from wall.models import Post, Comment
from sockets.models import Channel

categories = (
    ('like', 'like'),
    ('comment', 'comment'),
    ('dm', 'dm'),
)


class Notification(models.Model):
    category = models.TextField(choices=categories, default="")
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, null=True, blank=True, on_delete=models.CASCADE)
    user_receiving = models.ForeignKey(User, related_name='user_receiving', on_delete=models.CASCADE)
    user_sending = models.ForeignKey(User, related_name='user_sending', on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.post and self.comment:
            return f'{self.user_sending} commented on post-{self.post.id} from {self.user_receiving}'
        elif self.post:
            return f'{self.user_sending} liked post-{self.post.id} from {self.user_receiving}'
        elif self.channel:
            return f'{self.user_sending} sent a message to {self.user_receiving}'
        else:
            return f'Empty'
