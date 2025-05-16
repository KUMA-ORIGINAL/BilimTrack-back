from django.contrib import admin

from unfold.admin import ModelAdmin as UnfoldModelAdmin

from ..models import Group


@admin.register(Group)
class GroupAdmin(UnfoldModelAdmin):
    list_display = ('id', 'name', 'points')
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    autocomplete_fields = ('subjects',)
