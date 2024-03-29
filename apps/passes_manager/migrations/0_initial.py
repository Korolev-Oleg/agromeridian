# Generated by Django 3.1.2 on 2020-10-12 21:16

import apps.passes_manager.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Почта')),
                ('token', models.CharField(default=uuid.uuid4, max_length=36, verbose_name='Токен')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Создано')),
                ('is_registered', models.BooleanField(default=True, verbose_name='Зарегистрирован')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=500, verbose_name='Собственник')),
                ('car_number', models.CharField(max_length=8, verbose_name='Номер машины')),
                ('zone', models.CharField(choices=[('m', 'Мкад'), ('t', 'ТТК'), ('s', 'СК')], max_length=1)),
                ('sts', models.FileField(upload_to=apps.passes_manager.models.get_unique_filename, verbose_name='СТС')),
                ('pts', models.FileField(upload_to=apps.passes_manager.models.get_unique_filename, verbose_name='ПТС')),
                ('dk', models.FileField(upload_to=apps.passes_manager.models.get_unique_filename, verbose_name='ДК')),
                ('vu', models.FileField(upload_to=apps.passes_manager.models.get_unique_filename, verbose_name='ВУ')),
                ('owner_passport', models.FileField(upload_to=apps.passes_manager.models.get_unique_filename, verbose_name='Паспорт собственника ТС')),
                ('lsnnl', models.FileField(upload_to=apps.passes_manager.models.get_unique_filename, verbose_name='ЛЩННГ')),
                ('requisites', models.FileField(upload_to=apps.passes_manager.models.get_unique_filename, verbose_name='Реквизиты')),
                ('date_push_onetime', models.DateField(verbose_name='Дата подачи на разовый')),
                ('date_push_year', models.DateField(verbose_name='Дата подачи на годовой')),
                ('date_get_year', models.DateField(verbose_name='Дата выдачи годового')),
                ('comment', models.TextField(verbose_name='Комментарий')),
                ('is_passed', models.BooleanField(default=False, verbose_name='Выдан')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passes_manager.clients')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
    ]
