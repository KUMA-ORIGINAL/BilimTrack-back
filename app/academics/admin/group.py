from django.contrib import admin

from unfold.admin import ModelAdmin as UnfoldModelAdmin

from ..models import Group


@admin.register(Group)
class GroupAdmin(UnfoldModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
