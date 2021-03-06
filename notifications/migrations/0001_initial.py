# Generated by Django 3.1.5 on 2021-04-26 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=256)),
                ('read', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user_receiving', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_receiving', to=settings.AUTH_USER_MODEL)),
                ('user_sending', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_sending', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
