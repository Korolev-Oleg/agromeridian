from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User
from config import settings
from config.settings import EXTERNAL_TOKEN_VALIDATION_URL
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns

from core.utils import send_mail, get_unique_filename


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

    # Зявка пользователя
    sts = models.FileField(upload_to=get_unique_filename, verbose_name='СТС')
    pts = models.FileField(upload_to=get_unique_filename, verbose_name='ПТС')
    dk = models.FileField(upload_to=get_unique_filename, verbose_name='ДК')
    vu = models.FileField(upload_to=get_unique_filename, verbose_name='ВУ')
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
