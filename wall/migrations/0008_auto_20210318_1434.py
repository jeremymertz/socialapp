# Generated by Django 3.1.5 on 2021-03-18 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0007_auto_20210318_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(default=None, max_length=250, null=True),
        ),
    ]
