from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.decorators import display

from account.models import Tool


@admin.register(Tool)
class ToolAdmin(UnfoldModelAdmin):
    list_display = ('name', 'display_photo')

    @display(description=_("Фото"))
    def display_photo(self, obj):
        if obj.logo:
            return mark_safe(
                f'<img src="{obj.logo.url}" height="120" width="120" '
                f'style="border-radius: 10%;" />')