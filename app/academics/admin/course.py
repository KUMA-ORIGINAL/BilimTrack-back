from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from ..models import Course


@admin.register(Course)
class CourseAdmin(UnfoldModelAdmin):
    list_display = ('id', 'number', 'organization')
    list_filter = ('organization',)
    search_fields = ('number',)
