from django.contrib import admin

from unfold.admin import ModelAdmin as UnfoldModelAdmin

from ..models import Group


@admin.register(Group)
class GroupAdmin(UnfoldModelAdmin):
    list_display = ('id', 'name', 'organization', 'points')
    list_display_links = ('id', 'name',)
    list_filter = ('organization',)
    search_fields = ('name',)
    autocomplete_fields = ('subjects',)
