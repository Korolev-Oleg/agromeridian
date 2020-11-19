from django.contrib import admin
from django.contrib.auth.models import User

from .models import Applications
from .models import Clients
from config.settings import EXTERNAL_TOKEN_VALIDATION_URL
from config.settings import BASE_DIR

from core.utils import get_disk_usage


@admin.register(Applications)
class ApplicationsAdmin(admin.ModelAdmin):
    change_list_template = 'admin/custom_change_list.html'
    change_form_template = 'admin/custom_change_form.html'
    search_fields = ('owner', 'car_number')
    list_display = ('owner', 'car_number', 'zone', 'is_complete', 'is_passed',)
    list_filter = ('is_passed', 'zone', 'client', 'date_get_year')

    fieldsets = (
        (None, {
            'fields': (
                'owner',
                'car_number',
                'client',
                'zone',
            )
        }),
        ('Блок администрирования', {
            'fields': (
                'date_push_onetime',
                'date_push_year',
                'date_get_year',
                'comment_admin',
                ('is_passed', 'notify_client',),

            )
        }),
        ('Зявка пользователя', {
            'fields': (
                'sts',
                'pts',
                'dk',
                'vu',
                'owner_passport',
                'lsnnl',
                'requisites',
                'comment_from_user',
            )
        }),
    )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        disk = get_disk_usage(BASE_DIR)
        extra_context['disk_used'] = str(disk.used)[:4]
        extra_context['disk_total'] = str(disk.total)[:5]
        if (disk.total - disk.used) < 2:
            extra_context['disk_size_warning'] = True
        return super(ApplicationsAdmin, self).changelist_view(request, extra_context=extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = {}
        extra_context.setdefault(
            'get_zip_url',
            Applications.objects.get(pk=object_id).get_zip_url())

        return super(
            ApplicationsAdmin, self).changeform_view(
            request, object_id=object_id,
            form_url=form_url,
            extra_context=extra_context
        )


class UserInline(admin.TabularInline):
    model = User
    extra = False


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    change_form_template = 'admin/clients_change_form.html'
    list_display = ('__str__', 'is_registered', 'is_email_sent')

    def delete_queryset(self, request, queryset):
        for client in queryset:
            client.delete_own_user()
        queryset.delete()

    def render_change_form(self, request, context, *args, **kwargs):
        context['token_validation_url'] = EXTERNAL_TOKEN_VALIDATION_URL
        return super(ClientsAdmin, self).render_change_form(request, context, *args, **kwargs)
