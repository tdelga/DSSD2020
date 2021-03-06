# Generated by Django 3.1.1 on 2020-12-02 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0008_auto_20201021_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='miembro_proyecto',
            name='name',
        ),
        migrations.RemoveField(
            model_name='protocolo',
            name='proyecto',
        ),
        migrations.AddField(
            model_name='miembro_proyecto',
            name='boss',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='miembro_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='cantidad',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='protocolo',
            name='date_of_end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='protocolo',
            name='date_of_start',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='protocolo',
            name='status',
            field=models.CharField(default='pending', max_length=200),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='date_of_end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='date_of_start',
            field=models.DateTimeField(null=True),
        ),
        migrations.CreateModel(
            name='Proyecto_protocolo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protocolo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='protocolo_id', to='api.protocolo')),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyecto_id', to='api.proyecto')),
            ],
        ),
    ]
