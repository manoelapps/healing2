# Generated by Django 5.0.4 on 2024-04-20 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0004_alter_documento_consulta_avaliacoes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avaliacoes',
            name='avaliacao',
            field=models.CharField(choices=[('1', 'Muito Ruim'), ('2', 'Ruim'), ('3', 'Regular'), ('4', 'Bom'), ('5', 'Excelente')], default='', max_length=1),
        ),
    ]
