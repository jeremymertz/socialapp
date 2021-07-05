from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from PIL import Image
import os
import uuid


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]

    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('post', filename)


class Post(models.Model):
    content = models.TextField(max_length=250, default=None, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(timezone.now)
    picture = models.ImageField(default=None, upload_to=content_file_name)
    likes = models.ManyToManyField(User, related_name='likes', symmetrical=False, blank=True)
    hidden = models.BooleanField(default=True)

    def __str__(self):
        return f'Post {self.pk} by {self.user}'

    def get_absolute_url(self):
        return f"/post/{self.pk}/"

    def posted_ago(self):
        time_ago = timezone.now() - self.date_posted
        if time_ago.seconds < 60:
            return f'Just now'
        elif time_ago.days < 1 and time_ago.seconds < 3600 and (time_ago.seconds//60) < 60:
            return f'{time_ago.seconds//60} minutes ago' if time_ago.seconds//60 > 1 \
                else f'{time_ago.seconds//60} minute ago'
        elif time_ago.days < 1 and 60 < (time_ago.seconds // 60) < 1440:
            return f'{time_ago.seconds//3600} hours ago' if time_ago.seconds//3600 > 1 \
                else f'{time_ago.seconds//3600} hour ago'
        else:
            return f'{time_ago.days} days ago' if time_ago.days > 1 else f'{time_ago.days} day ago'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     output_size = (400, 400)
    #     img = Image.open(self.picture.path)
    #     if img.width > 400 or img.height > 400:
    #         img.thumbnail(output_size)
    #         img.save(self.picture.path)
    #     elif img.width < 400 or img.height < 400:
    #         img = img.resize(output_size)
    #         img.save(self.picture.path)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=250)
    date_posted = models.DateTimeField(timezone.now)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    like = models.ManyToManyField(User, related_name='comment_likes', symmetrical=False, blank=True)
    unlike = models.ManyToManyField(User, related_name='comment_unlikes', symmetrical=False, blank=True)
    ratio = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} commented: "{self.content}" on post {self.post.id} from {self.post.user.username}'

    def like_ratio(self):
        ratio = self.like.count() - self.unlike.count()
        return ratio

    def posted_ago(self):
        time_ago = timezone.now() - self.date_posted
        if time_ago.seconds < 60:
            return f'Just now'
        elif time_ago.days < 1 and time_ago.seconds < 3600 and (time_ago.seconds//60) < 60:
            return f'{time_ago.seconds//60} minutes ago' if time_ago.seconds//60 > 1 \
                else f'{time_ago.seconds//60} minute ago'
        elif time_ago.days < 1 and 60 < (time_ago.seconds // 60) < 1440:
            return f'{time_ago.seconds//3600} hours ago' if time_ago.seconds//3600 > 1 \
                else f'{time_ago.seconds//3600} hour ago'
        else:
            return f'{time_ago.days} days ago' if time_ago.days > 1 else f'{time_ago.days} day ago'



