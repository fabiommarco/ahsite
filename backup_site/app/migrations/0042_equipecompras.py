# Generated manually for EquipeCompras model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0041_auto_20200301_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipeCompras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('telefone', models.CharField(blank=True, max_length=20, verbose_name='Telefone')),
                ('ramal', models.CharField(blank=True, max_length=10, verbose_name='Ramal')),
                ('cargo', models.CharField(blank=True, max_length=100, verbose_name='Cargo')),
                ('local', models.CharField(blank=True, max_length=100, verbose_name='Local/Unidade')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('ordem', models.IntegerField(default=0, verbose_name='Ordem de Exibição')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
            ],
            options={
                'verbose_name': 'Membro da Equipe de Compras',
                'verbose_name_plural': 'Membros da Equipe de Compras',
                'ordering': ['ordem', 'nome'],
            },
        ),
    ] 