from django import forms
from django.core.exceptions import ValidationError

from .models import Applications


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=70, label='ФИО или наиминование организации')
    email = forms.EmailField(label='Почта')
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, label='Пароль')

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 8:
            raise ValidationError('Минимальная длина пароля 8 символов')

        if self.cleaned_data['email'].count(password):
            raise ValidationError('Пароль слишком похож на email!')

        return password


class PassesForm(forms.Form):
    class Zones:
        MCAD = 'm'
        TTK = 't'
        SK = 's'
        chooses = (('', ''), (MCAD, 'МКАД'), (TTK, 'ТТК'), (SK, 'СК'),)

    owner = forms.CharField(max_length=500, label='Собственник')
    car_number = forms.CharField(max_length=12, min_length=8, label='Номер машины')
    zone = forms.ChoiceField(choices=Zones.chooses, label='Зона')
    sts = forms.FileField(label='СТС', )
    pts = forms.FileField(label='ПТС', )
    dk = forms.FileField(label='ДК', )
    vu = forms.FileField(label='ВУ', )
    owner_passport = forms.FileField(
        label='Паспорт собственника ТС',
        help_text='Не обязательное поле',
        required=False
    )
    lsnnl = forms.FileField(
        label='Лизинг', help_text='Не обязательное поле',
        required=False
    )
    requisites = forms.FileField(
        label='Реквизиты', help_text='Не обязательное поле',
        required=False
    )
    additional_file = forms.FileField(
        label='Дополнительно', help_text='Не обязательное поле',
        required=False
    )
    comment_from_user = forms.CharField(widget=forms.Textarea, label='Комментарий', required=False)

    def __init__(self, *args, **kwargs):
        super(PassesForm, self).__init__(*args, **kwargs)
        self.fields['owner'].widget.attrs.update({'class': 'testlcasjnesohfeishfes'})
