from django.contrib import admin

from unfold.contrib.filters.admin import RelatedDropdownFilter

from academics.models import Grade
from common.admin import BaseModelAdmin


@admin.register(Grade)
class GradeAdmin(BaseModelAdmin):
    list_display = ('user', 'session', 'grade', 'comment', 'detail_link')  # отображаемые поля
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
