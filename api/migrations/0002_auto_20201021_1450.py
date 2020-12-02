# Generated by Django 3.1.1 on 2020-10-21 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='responsable',
        ),
        migrations.AddField(
            model_name='proyecto',
            name='miembro_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='proyecto_id', to='api.miembro_proyecto'),
        ),
        migrations.AlterField(
            model_name='actividades_protocolo',
            name='protocolo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='protocolo_actividad', to='api.protocolo'),
        ),
    ]