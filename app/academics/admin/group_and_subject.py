from django.contrib import admin
from ..models import Group, Subject

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')
    search_fields = ('name',)
    list_filter = ('group',)
