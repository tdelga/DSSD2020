# Generated by Django 3.1.3 on 2020-11-29 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protocolo',
            name='date_of_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='protocolo',
            name='date_of_start',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='date_of_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='date_of_start',
            field=models.DateTimeField(),
        ),
    ]