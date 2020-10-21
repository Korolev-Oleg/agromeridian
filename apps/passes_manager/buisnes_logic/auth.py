from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse

from apps.passes_manager.models import Clients
from config import settings
from core.utils import send_mail


def go_login(request):
    return HttpResponseRedirect(f'/accounts/login?email={request.GET["email"]}')


def go_admin():
    return HttpResponseRedirect(f'{settings.ADMIN_LOGIN_REDIRECT_URL}')


def go_register(request):
    return HttpResponseRedirect(f'/registration?email={request.GET["email"]}&token={request.GET["token"]}')


def go_cabinet():
    print(reverse('cabinet'))
    return HttpResponseRedirect(reverse('cabinet'))


def is_user_exist(username, email):
    user_name: bool
    user_email: bool
    try:
        User.objects.get(username=username)
        user_name = True
    except User.DoesNotExist:
        user_name = False

    try:
        User.objects.get(email=email)
        user_email = True
    except User.DoesNotExist:
        user_email = False

    return user_email or user_name


def set_registered_details(token, email, username):
    client = Clients.objects.get(token=token)
    if not client.email:
        client.email = email
    client.user = User.objects.get(email=email)
    client.name = username
    client.is_registered = True
    client.is_email_sent = True
    client.save()


def sent_register_detail(form):
    print('sent detail')
    message = f"Логин: {form.cleaned_data['email']}\n"
    message += f"Пароль: {form.cleaned_data['password']}\n"
    message += f"Ссылка для входа: {settings.EXTERNAL_LOGIN_URL}"
    if settings.DEBUG:
        print(message)
    else:
        send_mail('Данные для входа в agro-meridian', message=message, to=form.cleaned_data['email'])


def register_new_user(username, email, password):
    """ Сохраняет нового пользователя в модель User """
    if not is_user_exist(username, email):
        user = User.objects.create()
        user.username = email
        user.email = email
        user.first_name = username
        user.set_password(password)
        user.save()
        return True
    else:
        raise Exception(f'ПОЛЬЗОВАТЕЛЬ: {username} is exist')
