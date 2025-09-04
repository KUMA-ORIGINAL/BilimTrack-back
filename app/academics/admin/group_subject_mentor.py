from django.contrib import admin
from unfold.admin import TabularInline

from common.admin import BaseModelAdmin
from ..models import GroupSubjectMentor, GroupSubjectMentorSubject


class GroupSubjectMentorSubjectInline(TabularInline):
    model = GroupSubjectMentorSubject
    extra = 1
    fields = ('subject',)


@admin.register(GroupSubjectMentor)
class GroupSubjectMentorAdmin(BaseModelAdmin):
    list_display = ('id', 'group', 'mentor', 'created_at', 'updated_at', 'detail_link')
    list_display_links = ('id', 'group',)
    list_filter = ('group', 'mentor')
    search_fields = (
        'group__name',
        'mentor__username',
        'mentor__first_name',
        'mentor__last_name',
    )
    autocomplete_fields = ('group', 'mentor')
    inlines = (GroupSubjectMentorSubjectInline,)
