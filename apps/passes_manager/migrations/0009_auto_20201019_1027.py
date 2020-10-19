# Generated by Django 3.1.2 on 2020-10-19 10:27

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes_manager', '0008_auto_20201017_1504'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='applications',
            options={'ordering': ['-comment_admin', '-is_passed', '-pk'], 'verbose_name': 'Заявка', 'verbose_name_plural': 'Заявки'},
        ),
        migrations.AddField(
            model_name='applications',
            name='additional_file',
            field=models.FileField(blank=True, help_text='Не обязательное поле', null=True, upload_to=core.utils.get_unique_filename, verbose_name='Дополнительный файл'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='car_number',
            field=models.CharField(max_length=12, verbose_name='Номер машины'),
        ),
    ]
