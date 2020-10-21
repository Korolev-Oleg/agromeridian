import os
from pathlib import Path
from uuid import uuid4
from collections import namedtuple

from django.core.handlers.wsgi import WSGIRequest
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


def get_disk_usage(path):
    """Return disk usage statistics about the given path.

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in bytes.
    """
    _ntuple_diskusage = namedtuple('usage', 'total used free')
    st = os.statvfs(path)

    free = (st.f_bavail * st.f_frsize) / 1e+9
    total = (st.f_blocks * st.f_frsize) / 1e+9
    used = (st.f_blocks - st.f_bfree) * st.f_frsize / 1e+9

    return _ntuple_diskusage(total, used, free)
