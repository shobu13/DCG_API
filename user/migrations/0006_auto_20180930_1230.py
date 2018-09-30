# Generated by Django 2.1.1 on 2018-09-30 10:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_user_amis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='amis',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, upload_to='users/photos/'),
        ),
    ]
