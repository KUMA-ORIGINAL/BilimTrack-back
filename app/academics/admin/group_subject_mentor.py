from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from ..models import GroupSubjectMentor


@admin.register(GroupSubjectMentor)
class GroupSubjectMentorAdmin(UnfoldModelAdmin):
    list_display = ('id', 'group', 'subject', 'mentor', 'created_at', 'updated_at')
    list_display_links = ('id', 'group',)
    list_filter = ('group', 'subject', 'mentor')
    search_fields = (
        'group__name',
        'subject__name',
        'mentor__username',
        'mentor__first_name',
        'mentor__last_name',
    )
    autocomplete_fields = ('group', 'subject', 'mentor')
