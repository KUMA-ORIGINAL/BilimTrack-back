from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.decorators import display

from common.admin import BaseModelAdmin
from ..models import Semester


@admin.register(Semester)
class SemesterAdmin(BaseModelAdmin):
    list_display = ('id', 'number', 'course', 'start_date', 'end_date', 'detail_link')
    list_display_links = ('id', 'number')
    search_fields = ('course__organization__name', 'course__education_level__name')
    list_filter = ('course__organization', 'course__education_level')

    @display(description=_("Курс"))
    def display_course(self, obj):
        return f"{obj.course.number} курс ({obj.course.education_level})"
