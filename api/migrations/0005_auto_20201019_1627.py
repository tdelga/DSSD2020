# Generated by Django 3.1.1 on 2020-10-19 19:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20201017_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='protocolo',
            name='fecha_de_creacion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='protocolo',
            name='puntaje',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
