from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from ..models import Organization


@admin.register(Organization)
class OrganizationAdmin(UnfoldModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
