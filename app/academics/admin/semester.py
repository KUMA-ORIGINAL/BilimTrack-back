from django.contrib import admin

from account.models import ROLE_ADMIN
from common.admin import BaseModelAdmin
from .filters import EducationLevelFilter, CourseFilter
from ..models import Semester


class CourseEducationLevelFilter(EducationLevelFilter):

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(course__education_level_id=self.value())
        return queryset


@admin.register(Semester)
class SemesterAdmin(BaseModelAdmin):
    list_display = ('id', 'number', 'course', 'start_date', 'end_date', 'detail_link')
    list_display_links = ('id', 'number')
    search_fields = ('course__organization__name', 'course__education_level__name')
    autocomplete_fields = ('course',)
    list_select_related = ('course',)

    def get_list_filter(self, request):
        list_filter = ('course__organization', 'course__education_level', 'course')
        if request.user.role == ROLE_ADMIN:
            list_filter = (CourseEducationLevelFilter, CourseFilter)
        return list_filter

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == ROLE_ADMIN:
            return qs.filter(course__organization_id=request.user.organization_id)
        return qs.none()
