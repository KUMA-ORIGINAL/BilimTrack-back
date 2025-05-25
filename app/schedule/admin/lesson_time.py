from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from ..models import (
    LessonTime,
)


@admin.register(LessonTime)
class LessonTimeAdmin(UnfoldModelAdmin):
    list_display = ('id', 'start_time', 'end_time')
    list_display_links = ('id', 'start_time', 'end_time')

