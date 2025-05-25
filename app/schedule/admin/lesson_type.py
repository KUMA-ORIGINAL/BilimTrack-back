from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from ..models import LessonType


@admin.register(LessonType)
class LessonTypeAdmin(UnfoldModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
