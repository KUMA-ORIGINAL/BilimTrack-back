from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from account.models import ROLE_ADMIN
from common.admin import BaseModelAdmin
from ..models import Semester


@admin.register(Semester)
class SemesterAdmin(BaseModelAdmin):
    list_display = ('id', 'number', 'course', 'start_date', 'end_date', 'detail_link')
    list_display_links = ('id', 'number')
    search_fields = ('course__organization__name', 'course__education_level__name')
    list_filter = ('course__organization', 'course__education_level', 'course')
    autocomplete_fields = ('course',)
    list_select_related = ('course',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == ROLE_ADMIN:
            return qs.filter(course__organization_id=request.user.organization_id)
        return qs.none()
