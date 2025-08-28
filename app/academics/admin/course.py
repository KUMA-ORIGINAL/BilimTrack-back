from django.contrib import admin

from common.admin import BaseModelAdmin
from ..models import Course


@admin.register(Course)
class CourseAdmin(BaseModelAdmin):
    list_display = ('id', 'number', 'organization', 'education_level', 'detail_link')
    list_filter = ('organization', 'education_level')
    search_fields = ('number',)
