# Generated by Django 3.1.5 on 2021-03-19 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0008_auto_20210318_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hidden',
            field=models.BooleanField(default=True),
        ),
    ]