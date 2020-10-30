import os
from pathlib import Path
from uuid import uuid4
from collections import namedtuple
from smtplib import SMTPAuthenticationError

from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import send_mail as django_send_mail
from config import settings
from loguru import logger
from pathlib import Path


def get_full_url(url):
    return f"{settings.FULL_EXTERNAL_HOST.removesuffix('/')}/{url.removeprefix('/')}"


def send_mail(subject='Сообщение от agro-meridian', message='', to=list) -> None:
    if not isinstance(to, list):
        to = [to]

    message += '\n\nСпасибо за использование сервиса получения пропусков - http://agro-meridian.com!'
    message += '\nСообщение сгенерированно автоматически просьба не отвечать на него.'
    try:
        django_send_mail(
            message=message,
            subject=subject,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=to)
    except SMTPAuthenticationError:
        logger.error(f'SMTPAuthenticationError: \nsubject: {subject}\nmessage: {message}\nto: {to}')


def new_passes_notification_to_admin_email(client: str, owner: str, comment: str, car_number: str, url: str):
    """
    Оповещает админа о новой заявке
    """
    message = f'Собственник: {owner}\n'
    message += f'Номер машины: {car_number}\n'
    message += f'Комментарий: {comment}\n'
    message += f'Просмотр: {get_full_url(url)}\n'
    send_mail(subject=f'Новая заявка от {client}', message=message, to=settings.ADMIN_EMAIL)


def send_notification_for_client(application):
    """
    Оповещает клиента о комментарии от админа к заявке
    """
    message = f'Администратор оставил комментарий к заявке:\n'
    message += f'{application.comment_admin}\n'

    if application.date_get_year:
        message += f'\nДата выдачи годового: {application.date_get_year}'

    if application.date_push_year:
        message += f'\nДата подачи на годовой: {application.date_push_year}'

    if application.date_push_onetime:
        message += f'\nДата подачи на разовый: {application.date_push_onetime}'

    message += f'\nПросмотр: {get_full_url(application.get_absolute_url())}'
    send_mail(
        subject=f'Сообщение от администратора agro-meridian: {application.car_number}',
        message=message,
        to=application.client.email)


def get_unique_filename(instance=None, filename=''):
    """
    Именует медиа файлы <uuid + filename.suffix>
    """
    return f'{uuid4()}{Path(filename).suffix}'


def handle_uploaded_file(f):
    with open(settings.MEDIA_ROOT / 'file.txt', 'w') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def logging_base_view(view):
    def decorator():
        try:
            return view()
        except Exception as error_message:
            settings.logger.error(error_message)


def get_disk_usage(path):
    """Return disk usage statistics about the given path.

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in bytes.
    """

    def get_size(start_path=path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        return total_size

    _ntuple_diskusage = namedtuple('usage', 'total used free')
    st = os.statvfs(path)

    free = (st.f_bavail * st.f_frsize) / 1e+9
    total = 12
    used = get_size() / 1e+9

    return _ntuple_diskusage(total, used, free)
