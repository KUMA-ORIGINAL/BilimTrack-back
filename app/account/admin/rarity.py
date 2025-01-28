from django.contrib import admin

from unfold.admin import ModelAdmin as UnfoldModelAdmin

from ..models import Rarity


@admin.register(Rarity)
class RarityAdmin(UnfoldModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
