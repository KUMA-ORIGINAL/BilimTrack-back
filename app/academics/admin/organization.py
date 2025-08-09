from django.contrib import admin

from common.admin import BaseModelAdmin
from ..models import Organization


@admin.register(Organization)
class OrganizationAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'detail_link')
    search_fields = ('name',)
