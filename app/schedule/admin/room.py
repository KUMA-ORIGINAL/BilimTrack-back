from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from ..models import (
    Room,
)


@admin.register(Room)
class RoomAdmin(UnfoldModelAdmin):
    list_display = ('id', 'building', 'number')
    list_display_links = ('id', 'building', 'number')
    search_fields = ('building', 'number')
