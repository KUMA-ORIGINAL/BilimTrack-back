from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from unfold.decorators import display

from common.admin import BaseModelAdmin
from ..models import Subject


@admin.register(Subject)
class SubjectAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'description', 'organization', 'display_photo', 'detail_link')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('organization',)

    @display(description=_("Фото"))
    def display_photo(self, obj):
        if obj.photo:
            return mark_safe(
                f'<img src="{obj.photo.url}" height="120" width="120" '
                f'style="border-radius: 10%;" />')
