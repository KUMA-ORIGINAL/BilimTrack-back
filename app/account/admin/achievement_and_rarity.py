from django.contrib import admin
from django.utils.html import format_html

from ..models import Rarity, Achievement


@admin.register(Rarity)
class RarityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'rarity', 'created_at', 'photo_thumbnail')
    list_filter = ('rarity',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'photo_thumbnail')

    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="100" height="100" />', obj.photo.url)
        return "Нет изображения"

    photo_thumbnail.short_description = 'Миниатюра'
