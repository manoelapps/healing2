# Generated by Django 5.0.4 on 2024-04-20 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0007_alter_consulta_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consulta',
            name='status',
            field=models.CharField(choices=[('A', 'Agendada'), ('F', 'Finalizada'), ('C', 'Cancelada'), ('I', 'Iniciada')], default='A', max_length=1),
        ),
    ]
