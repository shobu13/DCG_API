# Generated by Django 2.1.1 on 2018-11-16 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_auto_20181021_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]