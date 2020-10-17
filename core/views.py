import functools
import traceback

from django.core.handlers.wsgi import WSGIRequest
from django.db import transaction
from django.http import JsonResponse
from config import settings

JSON_DUMPS_PARAMS = {
    'ensure_ascii': False
}


def ret(json_object, status=200):
    return JsonResponse(
        json_object,
        status=status,
        safe=not isinstance(json_object, list),
        json_dumps_params=JSON_DUMPS_PARAMS
    )


def errors_response(exception):
    """
    Форматирует HTTP Ответ с описанием ошибки и Traceback
    """
    res = {'errorMessage': str(exception), }
    if settings.DEBUG:
        res.update({'traceback': traceback.format_exc()})

    return ret(res, status=400)


# def base_view(fn):
#     """
#     Декоратор для всех вьюшек, обрабатывает исключения
#     """
#     @functools.wraps(fn)
#     def inner(request: WSGIRequest, *args, **kwargs):
#         try:
#             with transaction.atomic():
#                 return fn(request, *args, **kwargs)
#         except Exception as e:
#             return errors_response(e)
#
#     return inner

def base_view(fn):
    """
    Декоратор для всех вьюшек, обрабатывает исключения
    """

    @functools.wraps(fn)
    def inner(request: WSGIRequest, *args, **kwargs):
        print(request.GET['STOPADMIN'])
        return fn(request, *args, **kwargs)

    return inner


def cls(request: WSGIRequest):
    from django.contrib.auth.models import User
    if request.GET.get('t190n20ms', None):
        pass