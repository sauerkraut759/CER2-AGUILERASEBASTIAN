# Generated by Django 5.2.1 on 2025-06-02 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_solicitudretiro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudretiro',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('en_ruta', 'En ruta'), ('completado', 'Completado')], default='pendiente', max_length=20),
        ),
        migrations.AlterField(
            model_name='solicitudretiro',
            name='fecha_estimada',
            field=models.DateField(),
        ),
    ]
