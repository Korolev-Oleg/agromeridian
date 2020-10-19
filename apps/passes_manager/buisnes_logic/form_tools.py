from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponseRedirect
from django.urls import reverse

from apps.passes_manager.models import Clients, Applications


def save_files_session(request: WSGIRequest, pk):
    # session_passes = request.session.get('passes', {})
    # session_passes[pk] = {}

    for filename in request.FILES:
        # session_passes[pk]['filename'] = []
        print(type(request.FILES[filename]))
        # for chunk in request.FILES[filename].chunks():

        # passes[pk] = chunk
        # print(chunk[:10])

    request.session.modified = True


def HARD_SAVE_FORM(request: WSGIRequest, model):
    print('HARD SAVE')
    if not model:
        model = Applications()

    # FILES SET
    sts_file = request.FILES.get('sts')
    pts_file = request.FILES.get('pts')
    dk_file = request.FILES.get('dk')
    vu_file = request.FILES.get('vu')
    owner_passport_file = request.FILES.get('owner_passport')
    lsnnl_file = request.FILES.get('lsnnl')
    requisites_file = request.FILES.get('requisites')
    additional_file = request.FILES.get('additional_file')

    # FIELDS SET
    owner_field = request.POST.get('owner')
    car_number_field = request.POST.get('car_number')
    zone_field = request.POST.get('zone')
    print('zone_field')
    print(zone_field)
    print(zone_field)
    print(zone_field)
    print(zone_field)
    comment_from_user_field = request.POST.get('comment_from_user')

    # SAVE FILES
    if sts_file:
        model.sts = sts_file
    if pts_file:
        model.pts = pts_file
    if dk_file:
        model.dk = dk_file
    if vu_file:
        model.vu = vu_file
    if owner_passport_file:
        model.owner_passport = owner_passport_file
    if lsnnl_file:
        model.lsnnl = lsnnl_file
    if requisites_file:
        model.requisites = requisites_file
    if additional_file:
        model.additional_file = additional_file

    # SAVE FIELDS
    if owner_field:
        model.owner = owner_field
    if car_number_field:
        model.car_number = car_number_field
    if zone_field:
        model.zone = zone_field
    if comment_from_user_field:
        model.comment_from_user = comment_from_user_field

    model.save()


def save_passes_form(model, form, user_pk):
    """
    Сохраняет данные формы заявки на пропуск в модель
    """
    print('SOFT SAVE')

    if not model:
        model = Applications()

    model.owner = form.cleaned_data['owner']
    model.car_number = form.cleaned_data['car_number']
    model.client = Clients.objects.get(user=user_pk)
    model.sts = form.cleaned_data['sts']
    model.pts = form.cleaned_data['pts']
    model.dk = form.cleaned_data['dk']
    model.vu = form.cleaned_data['vu']
    model.zone = form.cleaned_data['zone']
    model.owner_passport = form.cleaned_data['owner_passport']
    model.lsnnl = form.cleaned_data['lsnnl']
    model.requisites = form.cleaned_data['requisites']
    model.comment_from_user = form.cleaned_data['comment_from_user']
    model.additional_file = form.cleaned_data['additional_file']
    model.save()


def get_passes_initial(model) -> dict:
    """
    Формирует словарь текущих данных для передачи в форму
    return: {}
    """
    if model:
        print(model)
        initial = {
            'has_urls': True,
            'owner': model.owner,
            'car_number': model.car_number,
            'zone': model.zone,
            'sts': model.sts.readlines(),
            'pts': model.pts.readlines() if model.pts else None,
            'dk': model.dk.readlines() if model.dk else None,
            'vu': model.vu.readlines() if model.vu else None,
            'owner_passport': model.owner_passport.readlines() if model.owner_passport else None,
            'lsnnl': model.lsnnl.readlines() if model.lsnnl else None,
            'requisites': model.requisites.readlines() if model.requisites else None,
            'comment_from_user': model.comment_from_user
        }
    else:
        initial = {}

    return initial


def get_files_urls(model):
    """
    Формирует именнованный объект для получения ссылок на файлы в темплейте
    """

    class Urls:
        if model.sts:
            sts = model.sts.url
        if model.pts:
            pts = model.pts.url
        if model.dk:
            dk = model.dk.url
        if model.vu:
            vu = model.vu.url
        if model.owner_passport:
            owner_passport = model.owner_passport.url
        if model.lsnnl:
            lsnnl = model.lsnnl.url
        if model.requisites:
            requisites = model.requisites.url
        if model.additional_file:
            additional_file = model.additional_file
        if model.is_passed:
            is_passed = model.is_passed

    return Urls
