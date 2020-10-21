# Generated by Django 3.1.2 on 2020-10-21 08:00

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes_manager', '0009_auto_20201019_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='dk',
            field=models.FileField(blank=True, null=True, upload_to=core.utils.get_unique_filename, verbose_name='ДК'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='pts',
            field=models.FileField(blank=True, null=True, upload_to=core.utils.get_unique_filename, verbose_name='ПТС'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='sts',
            field=models.FileField(blank=True, null=True, upload_to=core.utils.get_unique_filename, verbose_name='СТС'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='vu',
            field=models.FileField(blank=True, null=True, upload_to=core.utils.get_unique_filename, verbose_name='ВУ'),
        ),
    ]