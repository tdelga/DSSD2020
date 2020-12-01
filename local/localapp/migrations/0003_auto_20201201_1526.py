# Generated by Django 3.1.3 on 2020-12-01 18:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localapp', '0002_auto_20201129_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='cantidad',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='protocolo',
            name='date_of_end',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='protocolo',
            name='date_of_start',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='date_of_end',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='date_of_start',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]