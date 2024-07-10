# Generated by Django 5.0.4 on 2024-07-08 19:26

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaSetor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Setor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('recebe_chamado', models.BooleanField(default=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=20)),
                ('telefone', phonenumber_field.modelfields.PhoneNumberField(default='+55', max_length=128, region='BR')),
                ('nivel', models.CharField(choices=[('adm_sistema', 'Administrador do Sistema'), ('adm', 'Administrador do Setor'), ('funcionario', 'Funcionário')], max_length=25)),
                ('status', models.BooleanField(default=True)),
                ('area_setor', models.ForeignKey(limit_choices_to={'status': True}, on_delete=django.db.models.deletion.CASCADE, to='home.areasetor')),
                ('setor', models.ForeignKey(limit_choices_to={'status': True}, on_delete=django.db.models.deletion.CASCADE, to='home.setor')),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.funcionario')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chamado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=280)),
                ('status', models.BooleanField(default=False)),
                ('data_abertura', models.DateTimeField(auto_now_add=True)),
                ('data_fechamento', models.DateTimeField(blank=True, null=True)),
                ('funcionario_abriu', models.ForeignKey(limit_choices_to={'status': True}, on_delete=django.db.models.deletion.CASCADE, related_name='chamados_abertos', to='home.funcionario')),
                ('funcionario_fechou', models.ForeignKey(blank=True, limit_choices_to={'status': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chamados_fechados', to='home.funcionario')),
                ('setor', models.ForeignKey(limit_choices_to={'recebe_chamado': True, 'status': True}, on_delete=django.db.models.deletion.CASCADE, to='home.setor')),
            ],
        ),
        migrations.AddField(
            model_name='areasetor',
            name='setor',
            field=models.ForeignKey(limit_choices_to={'status': True}, on_delete=django.db.models.deletion.CASCADE, to='home.setor'),
        ),
    ]