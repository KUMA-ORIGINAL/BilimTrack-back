from django.contrib import admin

from unfold.admin import ModelAdmin as UnfoldModelAdmin

from account.models import Skill


@admin.register(Skill)
class SkillAdmin(UnfoldModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
