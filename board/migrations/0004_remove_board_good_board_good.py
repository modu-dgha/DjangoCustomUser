# Generated by Django 4.1.2 on 2022-10-11 02:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0003_board_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='good',
        ),
        migrations.AddField(
            model_name='board',
            name='good',
            field=models.ManyToManyField(related_name='good_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
