from django.contrib import admin


from common.admin import BaseModelAdmin
from ..models import Group


@admin.register(Group)
class GroupAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'points', 'organization', 'education_level', 'detail_link')
    list_display_links = ('id', 'name',)
    list_filter = ('organization', 'education_level')
    search_fields = ('name',)
