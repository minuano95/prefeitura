# Generated by Django 5.0.4 on 2024-07-13 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamado',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='chamado',
            name='descricao_solucao',
            field=models.CharField(blank=True, default='', max_length=280, null=True),
        ),
    ]
