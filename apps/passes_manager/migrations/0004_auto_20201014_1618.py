# Generated by Django 3.1.2 on 2020-10-14 16:18

import apps.passes_manager.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('passes_manager', '0003_auto_20201014_0939'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applications',
            name='comment',
        ),
        migrations.AddField(
            model_name='applications',
            name='comment_from_user',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий от пользователя'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passes_manager.clients', verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='lsnnl',
            field=models.FileField(blank=True, help_text='Не обязательное поле', null=True, upload_to=apps.passes_manager.models.get_unique_filename, verbose_name='Лизинг'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='owner_passport',
            field=models.FileField(blank=True, help_text='Не обязательное поле', null=True, upload_to=apps.passes_manager.models.get_unique_filename, verbose_name='Паспорт собственника ТС'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='requisites',
            field=models.FileField(blank=True, help_text='Не обязательное поле', null=True, upload_to=apps.passes_manager.models.get_unique_filename, verbose_name='Реквизиты'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='zone',
            field=models.CharField(choices=[('m', 'Мкад'), ('t', 'ТТК'), ('s', 'СК')], max_length=1, verbose_name='Зона'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='name',
            field=models.CharField(blank=True, max_length=130, null=True, verbose_name='Наименование'),
        ),
    ]