from django.contrib import admin
from unfold.admin import TabularInline

from account.models import ROLE_ADMIN
from common.admin import BaseModelAdmin
from ..models import GroupSubjectMentor, GroupSubjectMentorSubject


class GroupSubjectMentorSubjectInline(TabularInline):
    model = GroupSubjectMentorSubject
    extra = 1
    fields = ('subject',)
    autocomplete_fields = ('subject',)


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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == ROLE_ADMIN:
            return qs.filter(group__organization_id=request.user.organization_id)
        return qs.none()
