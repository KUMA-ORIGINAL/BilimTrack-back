from django.contrib import admin

from unfold.admin import ModelAdmin as UnfoldModelAdmin

from ..models import Subject


@admin.register(Subject)
class SubjectAdmin(UnfoldModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
