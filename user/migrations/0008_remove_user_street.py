# Generated by Django 2.1.7 on 2019-03-25 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_user_est_verif'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='street',
        ),
    ]
