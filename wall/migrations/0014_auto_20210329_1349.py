# Generated by Django 3.1.5 on 2021-03-29 12:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wall', '0013_auto_20210324_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='unlike',
            field=models.ManyToManyField(blank=True, related_name='comment_unlikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile/default.jpg', upload_to='profile'),
        ),
    ]