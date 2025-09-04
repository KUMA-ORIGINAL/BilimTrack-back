from django.contrib import admin

from unfold.contrib.filters.admin import RelatedDropdownFilter

from academics.models import Grade
from account.models import ROLE_ADMIN
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
    autocomplete_fields = ('user', 'session')
    list_filter_submit = True
    list_per_page = 50

    fieldsets = (
        (None, {
            'fields': ('user', 'session', 'grade', 'comment')
        }),
        ('Таймстемпы', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # сворачиваемая секция
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == ROLE_ADMIN:
            return qs.filter(user__organization_id=request.user.organization_id)
        return qs.none()
