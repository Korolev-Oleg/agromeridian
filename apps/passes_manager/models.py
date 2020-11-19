import os
import zipfile
from collections import namedtuple
from pathlib import Path
from typing import Tuple
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User
from django.http import Http404
from slugify import slugify

from config import settings
from config.settings import EXTERNAL_TOKEN_VALIDATION_URL
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns

from core.utils import send_mail, get_unique_filename, send_notification_for_client
from core import utils
from config.settings import logger


class Applications(models.Model):
    """
    Модель заявок на пропуска, может обрабатывать комментарии менеджера.
    """

    class Zones:
        MCAD = 'm'
        TTK = 't'
        SK = 's'
        chooses = ((MCAD, 'МКАД'), (TTK, 'ТТК'), (SK, 'СК'),)

    #
    owner = models.CharField(max_length=500, verbose_name='Собственник')
    car_number = models.CharField(max_length=12, verbose_name='Номер машины')
    zone = models.CharField(max_length=1, choices=Zones.chooses, verbose_name='Зона')
    client = models.ForeignKey('Clients', on_delete=models.CASCADE, verbose_name='Клиент')

    # Блок администрирования
    date_push_onetime = models.DateField(verbose_name='Дата подачи на разовый', blank=True, null=True)
    date_push_year = models.DateField(verbose_name='Дата подачи на годовой', blank=True, null=True)
    date_get_year = models.DateField(verbose_name='Дата выдачи годового', blank=True, null=True)
    comment_admin = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    is_passed = models.BooleanField(default=False, verbose_name='Пропуск выдан')
    notify_client = models.BooleanField(default=False, verbose_name='Уведомить клиента')

    # Зявка пользователя
    sts = models.FileField(upload_to=get_unique_filename, verbose_name='СТС', blank=True, null=True)
    pts = models.FileField(upload_to=get_unique_filename, verbose_name='ПТС', blank=True, null=True)
    dk = models.FileField(upload_to=get_unique_filename, verbose_name='ДК', blank=True, null=True)
    vu = models.FileField(upload_to=get_unique_filename, verbose_name='ВУ', blank=True, null=True)
    owner_passport = models.FileField(
        upload_to=get_unique_filename, verbose_name='Паспорт собственника ТС',
        help_text='Не обязательное поле', blank=True, null=True)

    lsnnl = models.FileField(
        upload_to=get_unique_filename, verbose_name='Лизинг',
        help_text='Не обязательное поле', blank=True, null=True
    )
    requisites = models.FileField(
        upload_to=get_unique_filename, verbose_name='Реквизиты',
        help_text='Не обязательное поле', blank=True, null=True
    )
    additional_file = models.FileField(
        upload_to=get_unique_filename, verbose_name='Дополнительный файл',
        help_text='Не обязательное поле', blank=True, null=True
    )

    comment_from_user = models.TextField(verbose_name='Комментарий от пользователя', blank=True, null=True)

    def is_complete(self):
        if self.sts and self.pts and self.dk and self.vu:
            return True

    is_complete.boolean = True
    is_complete.short_description = 'Заполнено'

    def __str__(self):
        return self.owner

    def get_zone(self):
        """
        Возвращает строковое представление выбранной зоны
        """
        for zone_tuple in self.Zones.chooses:
            if zone_tuple[0] == self.zone:
                return zone_tuple[1]

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('passes-renew', args=[str(self.id)])

    @logger.catch()
    def __get_documents(self) -> list:

        def get_named_tuple(obj):
            """ Генерирует именнованный кортеж
                return: (name:str, path:str)
            """
            _tuple = namedtuple(
                typename=f'f_{uuid4().__str__()[:5]}',
                field_names=['name', 'path'])

            name = "{filename}{suffix}".format(
                filename=obj.field.name,
                suffix=Path(obj.name).suffix,
            )
            logger.debug(name)
            return _tuple(name=name, path=obj.path)

        documents = []
        if self.sts:
            documents.append(get_named_tuple(self.sts))
        if self.pts:
            documents.append(get_named_tuple(self.pts))
        if self.dk:
            documents.append(get_named_tuple(self.dk))
        if self.vu:
            documents.append(get_named_tuple(self.vu))
        if self.owner_passport:
            documents.append(get_named_tuple(self.owner_passport))
        if self.lsnnl:
            documents.append(get_named_tuple(self.lsnnl))
        if self.requisites:
            documents.append(get_named_tuple(self.requisites))
        if self.additional_file:
            documents.append(get_named_tuple(self.additional_file))

        logger.debug(documents)

        return documents

    def get_zip_url(self):
        return reverse('get-zip', args=[str(self.id)])

    def get_zip(self) -> namedtuple:
        zip_path = self.__make_zip()
        if zip_path.exists():
            with open(zip_path, 'rb') as _zip:
                return namedtuple(
                    'name', ['name', 'bytes'])(
                    name=zip_path.name,
                    bytes=_zip.read()
                )

        raise Http404

    @logger.catch()
    def __make_zip(self):
        """ Создает архив из файлов заявки
            return: Path - absolute system path to zip file
        """
        zip_dir = settings.MEDIA_ROOT / 'zip'
        if zip_dir.exists():
            os.system(f'rm -rf {zip_dir}')
            os.system(f'mkdir {zip_dir}')
        else:
            os.system(f'mkdir {zip_dir}')

        zip_name = '{name}_{car}_{zone}.zip'.format(
            name=slugify(self.owner),
            car=slugify(self.car_number),
            zone=slugify(self.get_zone()),
        )

        zip_path = zip_dir / zip_name
        with zipfile.ZipFile(zip_path, 'w') as _zip:
            for document in self.__get_documents():
                _zip.write(document.path, document.name)

        return zip_path

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.notify_client:
            # Уведомление для клиента
            send_notification_for_client(self)
            self.notify_client = False

        super(Applications, self).save()

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-comment_admin', '-is_passed', '-pk']


class Clients(models.Model):
    """
    Менеджер создает токен, из которого в change_form.html генеририруется ссылка
    Ссылка отправляется на почту клиенту автоматически если она была указана при создании
    После завершения регистрации is_registered присваевается True
    """
    token = models.CharField(max_length=36, verbose_name='Токен', default=uuid4)
    email = models.EmailField(blank=True, null=True, verbose_name='Почта', unique=True,
                              help_text='После сохранения, на эту почту будет отправлена ссылка для регистрации')

    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Создано')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, editable=False)
    name = models.CharField(max_length=130, blank=True, null=True, verbose_name='Наименование')
    is_registered = models.BooleanField(default=False, verbose_name='Зарегистрирован', editable=False)
    is_email_sent = models.BooleanField(default=False, verbose_name='Сообщение отправлено', editable=False)

    def __str__(self):
        """
        Возвращает форматированную дату либо email / user_firstname
        """
        if self.user:
            return self.user.first_name
        elif self.email:
            return self.email
        else:
            return str(self.created.strftime('%d %h %Y %H:%M'))

    def save(self, *args, **kwargs):
        """
        Send email to clients after save object
        """
        if self.email and not self.is_registered and not self.is_email_sent:
            token_validation_url = f'{EXTERNAL_TOKEN_VALIDATION_URL}?token={self.token}&email={self.email}'
            message = f'Ссылка для регистрации:\n{token_validation_url}'
            if settings.DEBUG:
                print(message)
            else:
                send_mail('Регистрация на портале agro-meridian', message, self.email)
            self.is_email_sent = True
        super().save(*args, **kwargs)

    def delete_own_user(self):
        try:
            User.objects.get(email=self.email).delete()
        except User.DoesNotExist:
            print("ОШИБКА УДАЛЕНИЯ СВЯЗАННОГО ПОЛЬЗОВАТЕЛЯ")

    def delete(self, *args, **kwargs):
        self.delete_own_user()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
