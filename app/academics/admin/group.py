from django.contrib import admin


from common.admin import BaseModelAdmin
from ..models import Group


@admin.register(Group)
class GroupAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'organization', 'points', 'detail_link')
    list_display_links = ('id', 'name',)
    list_filter = ('organization',)
    search_fields = ('name',)
    autocomplete_fields = ('subjects',)
