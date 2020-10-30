from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import generic

from config import settings
from .buisnes_logic.form_tools import (
    save_passes_form, get_passes_initial,
    get_files_urls,
    HARD_SAVE_FORM)

from .models import Clients
from .models import Applications
from .forms import RegistrationForm
from .forms import PassesForm
from config.settings import EMAIL_HOST_USER

from .buisnes_logic import auth


@settings.logger.catch
def validate_registration_token(request):
    token = request.GET['token']
    email = request.GET["email"]

    #  И токен пользователя
    client = Clients.objects.get(token=token)
    if client:
        if not client.is_registered:
            return auth.go_register(request)
        else:
            # если зарегистрирован
            return auth.go_login(request)

    return HttpResponse(f'Неверный ключ доступа, обратитесь к администратору!\n{EMAIL_HOST_USER}')


@settings.logger.catch
def get_registration_form(request):
    error = ''
    token = request.GET.get('token', False)

    # Если форма была отправлена
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if not auth.is_user_exist(username, email):

                # Регистрация пользователя
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                try:
                    auth.register_new_user(username, email, password)
                    # отправка собщения ползователю с данными для входа
                    auth.sent_register_detail(form)

                    # смена статуса клиента на зарегистрирован
                    auth.set_registered_details(token, email, username)
                except IntegrityError:
                    error = f'Пользователь с данными: {username} уже существует!'

            else:
                error = f'Пользователь с данными: {username} уже существует!'

            params = f"password={form.cleaned_data['password']}"
            if not error:
                return auth.go_login(request)
    else:
        form = RegistrationForm(initial={'email': request.GET['email'], })

    return render(request, 'passes_manager/registration_form.html', {'form': form, 'error': error, 'token': token})


@settings.logger.catch
@login_required()
def login_redirect(request):
    if request.user.is_staff:
        print('redirect')
        return auth.go_admin()

    else:
        print('go to cabinrt')
        return auth.go_cabinet()


class UserPassesView(LoginRequiredMixin, generic.ListView):
    """
    Представление всех заявок пользователя
    """
    model = Applications
    # paginate_by = 5
    template_name = 'passes_manager/user_passes.html'
    context = {
        'test': 1111
    }

    def get_queryset(self):
        return Applications.objects.filter(client__user=self.request.user)

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        context['message'] = self.request.GET.get('message', '')
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )


def test(request, pk=1):
    return HttpResponse('success')


@settings.logger.catch
@login_required()
def renew_passes_form(request, pk=False):
    """
    Обрабатывает запросы на представление формы редактирования или заполнения
    заявок
    """
    is_new_form = not pk
    form = None
    db = None

    if not is_new_form:
        db = get_object_or_404(Applications, pk=pk)

    admin_comment = ''
    urls_to_files = ''
    if request.method == 'POST':
        # Валидация данных формы
        form = PassesForm(request.POST, request.FILES)
        if form.is_valid():
            pk_new = save_passes_form(db, form, request.user.pk)
            if is_new_form:
                return HttpResponseRedirect(
                    f"{reverse('cabinet')}?message=Заявка для машины {form.cleaned_data['car_number']} подана!")
            else:
                return HttpResponseRedirect(
                    f"{reverse('cabinet')}?message=Изменения внесены успешно!")

        else:
            print('HARD SAVE')
            HARD_SAVE_FORM(request, db)
            if is_new_form:
                return HttpResponseRedirect(f"{reverse('cabinet')}?message=Заявка подана!")
            else:
                return HttpResponseRedirect(f"{reverse('cabinet')}?message=Изменения внесены успешно!")

    elif request.method == 'GET':
        # новая форма
        if is_new_form:
            form = PassesForm(initial={'owner': request.user.first_name})

        # редактирование формы
        else:
            form = PassesForm(initial=get_passes_initial(db))
            urls_to_files = get_files_urls(db)
            admin_comment = db.comment_admin

    return render(request, 'passes_manager/passes_form.html',
                  {'form': form,
                   'admin_comment': admin_comment,
                   'urls_to_files': urls_to_files,
                   'is_new': is_new_form})
