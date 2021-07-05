# Generated by Django 3.1.5 on 2021-05-07 08:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sockets', '0005_auto_20210507_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='connected_users',
            field=models.ManyToManyField(blank=True, related_name='Connected_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
