from django.contrib import admin
from .models import Applications


# Register your models here.
@admin.register(Applications)
class AdminApplications(admin.ModelAdmin):
    change_list_template = 'admin/model_change_list.html'
    search_fields = ('test_field',)
