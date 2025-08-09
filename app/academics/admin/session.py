from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from common.admin import BaseModelAdmin
from ..models import Session


@admin.register(Session)
class SessionAdmin(BaseModelAdmin):
    list_display = ('id', 'subject', 'date', 'start_time', 'end_time', 'is_active', 'detail_link')
    list_display_links = ('id', 'subject')
    search_fields = ('subject__name',)
    list_filter = ('subject', 'is_active', 'date')

    @display(description=_("Предмет"))
    def display_subject(self, obj):
        return obj.subject.name

    @display(description=_("Время занятия"))
    def display_time(self, obj):
        return f"{obj.start_time} - {obj.end_time}"

    # Если хотите более красиво, добавьте display_subject и display_time в list_display:
    # list_display = ('id', 'display_subject', 'date', 'display_time', 'is_active')
