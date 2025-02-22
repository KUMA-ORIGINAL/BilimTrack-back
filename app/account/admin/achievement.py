from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.decorators import display

from ..models import Achievement, UserAchievement


@admin.register(Achievement)
class AchievementAdmin(UnfoldModelAdmin):
    list_display = ('name', 'rarity', 'created_at', 'display_photo')
    list_filter = ('rarity',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)

    @display(description=_("Фото"))
    def display_photo(self, obj):
        if obj.photo:
            return mark_safe(
                f'<img src="{obj.photo.url}" height="120" width="120" '
                f'style="border-radius: 10%;" />')


@admin.register(UserAchievement)
class UserAchievementAdmin(UnfoldModelAdmin):
    list_display = ('user', 'achievement', 'is_opened', 'opened_at')