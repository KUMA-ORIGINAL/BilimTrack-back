from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from ..models import (
    Schedule
)


@admin.register(Schedule)
class ScheduleAdmin(UnfoldModelAdmin):
    list_display = (
        'id', 'group', 'subject', 'teacher',
        'day_of_week', 'lesson_time', 'lesson_type', 'room'
    )
    list_display_links = ('id', 'group', 'subject')
    list_filter = ('day_of_week', 'lesson_type', 'group', 'teacher')
    search_fields = (
        'group__name',
        'subject__name',
        'teacher__full_name',
        'room__number',
    )
    autocomplete_fields = ('group', 'subject', 'teacher', 'room')
