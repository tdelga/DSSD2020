# Generated by Django 3.1.1 on 2020-10-22 00:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20201021_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protocolo',
            name='date_of_end',
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