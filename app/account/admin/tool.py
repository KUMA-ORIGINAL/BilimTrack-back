from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from account.models import Tool


@admin.register(Tool)
class ToolAdmin(UnfoldModelAdmin):
    list_display = ('name', )