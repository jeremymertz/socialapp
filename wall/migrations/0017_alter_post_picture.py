# Generated by Django 3.2.4 on 2021-06-28 07:53

from django.db import migrations, models
import wall.models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0016_comment_ratio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.ImageField(default=None, upload_to=wall.models.content_file_name),
        ),
    ]