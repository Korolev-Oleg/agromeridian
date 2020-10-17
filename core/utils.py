from pathlib import Path
from uuid import uuid4

from django.core.mail import send_mail as django_send_mail
from config import settings
from loguru import logger


def send_mail(subject='Сообщение от agro-meridian', message='', to=list) -> None:
    if not isinstance(to, list):
        to = [to]

    message += '\n\nСпасибо за использование сервиса получения пропусков - http://agro-meridian.com!'
    django_send_mail(
        message=message,
        subject=subject,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=to)


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
