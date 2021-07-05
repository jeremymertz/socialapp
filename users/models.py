from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from django.core.files.storage import default_storage as storage


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=400, blank=True)
    profile_picture = models.ImageField(default='profile/default.jpg', upload_to='profile', blank=True)
    followers = models.ManyToManyField(User, related_name='followed_by', symmetrical=False, blank=True)
    followings = models.ManyToManyField(User, related_name='following', symmetrical=False, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return f"/profile/{self.user.username}/"

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     output_size = (300, 300)
    #     img = Image.open(self.profile_picture)
    #     if img.width > 300 or img.height > 300:
    #         img.thumbnail(output_size)
    #         img.save(self.profile_picture.name)
    #
    #
