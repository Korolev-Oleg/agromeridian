# Generated by Django 3.1.2 on 2020-10-13 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes_manager', '0_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='email',
            field=models.EmailField(blank=True, help_text='После сохранения, на эту почту будет отправлена ссылка для регистрации', max_length=254, null=True, unique=True, verbose_name='Почта'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='is_registered',
            field=models.BooleanField(default=False, verbose_name='Зарегистрирован'),
        ),
    ]
