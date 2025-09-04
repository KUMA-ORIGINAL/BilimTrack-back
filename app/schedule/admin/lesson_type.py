from django.contrib import admin

from common.admin import BaseModelAdmin
from ..models import LessonType


@admin.register(LessonType)
class LessonTypeAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'detail_link')
    list_display_links = ('id', 'name')
