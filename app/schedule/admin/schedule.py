from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from ..models import Schedule

@admin.register(Schedule)
class ScheduleAdmin(UnfoldModelAdmin):
    list_display = (
        'id', 'get_groups', 'subject', 'teacher',
        'day_of_week', 'lesson_time', 'lesson_type', 'room'
    )
    list_display_links = ('id', 'subject')
    list_filter = (
        'day_of_week',
        'lesson_type',
        ('groups', admin.RelatedOnlyFieldListFilter),
        'teacher'
    )
    search_fields = (
        'subject__name',
        'teacher__full_name',
        'room__number',
    )
    autocomplete_fields = ('groups', 'subject', 'teacher', 'room')

    @admin.display(description='Группы')
    def get_groups(self, obj):
        return ", ".join([str(g) for g in obj.groups.all()])
