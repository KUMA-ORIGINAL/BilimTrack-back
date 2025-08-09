from django.contrib import admin

from common.admin import BaseModelAdmin
from ..models import Course


@admin.register(Course)
class CourseAdmin(BaseModelAdmin):
    list_display = ('id', 'number', 'organization', 'detail_link')
    list_filter = ('organization',)
    search_fields = ('number',)
