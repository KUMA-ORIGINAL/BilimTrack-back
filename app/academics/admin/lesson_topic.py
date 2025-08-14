from django.contrib import admin
from common.admin import BaseModelAdmin
from ..models import LessonTopic


@admin.register(LessonTopic)
class LessonTopicAdmin(BaseModelAdmin):
    list_display = ('id', 'title', 'subject', 'mentor', 'detail_link')
    list_display_links = ('id', 'title',)
    list_filter = ('subject', 'mentor')
    search_fields = ('title',)
    autocomplete_fields = ('subject', 'mentor')
