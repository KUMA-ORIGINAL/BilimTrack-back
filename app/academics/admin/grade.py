from django.contrib import admin

from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.contrib.filters.admin import RelatedDropdownFilter

from academics.models import Grade


@admin.register(Grade)
class GradeAdmin(UnfoldModelAdmin):
    list_display = ('user', 'session', 'grade', 'comment',)  # отображаемые поля
    ordering = ('-created_at',)  # сортировка по дате создания
    readonly_fields = ('created_at', 'updated_at')

    list_filter = (
        ("user", RelatedDropdownFilter),
        ("session", RelatedDropdownFilter),
        'grade',
        'created_at',
    )
    list_filter_submit = True

    fieldsets = (
        (None, {
            'fields': ('user', 'session', 'grade', 'comment')
        }),
        ('Таймстемпы', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # сворачиваемая секция
        }),
    )
