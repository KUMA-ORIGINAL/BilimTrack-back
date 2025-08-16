from django.contrib import admin
from unfold.admin import TabularInline

from common.admin import BaseModelAdmin
from ..models import Organization, EducationLevel


class EducationLevelInline(TabularInline):
    model = EducationLevel
    extra = 1
    fields = ("name",)
    show_change_link = True


@admin.register(Organization)
class OrganizationAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'detail_link')
    search_fields = ('name',)
    inlines = [EducationLevelInline]
