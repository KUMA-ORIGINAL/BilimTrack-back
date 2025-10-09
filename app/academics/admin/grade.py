from django.contrib import admin

from .filters import StudentDropdownFilter, SessionDropdownFilter
from academics.models import Grade
from account.models import ROLE_ADMIN
from common.admin import BaseModelAdmin


@admin.register(Grade)
class GradeAdmin(BaseModelAdmin):
    list_display = (
        'user',
        'session',
        'session_teacher',
        'session_subject',
        'grade',
        'attendance',
        'comment',
        'created_at',
        'detail_link'
    )
    ordering = ('-created_at',)  # сортировка по дате создания
    readonly_fields = ('created_at', 'updated_at')
    list_filter = (
        ("user", StudentDropdownFilter),
        ("session", SessionDropdownFilter),
        'grade',
        'created_at',
    )
    autocomplete_fields = ('user', 'session')
    list_select_related = ('user', 'session__subject', 'session__teacher')
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

    def session_subject(self, obj):
        return obj.session.subject

    session_subject.short_description = "Предмет"

    def session_teacher(self, obj):
        teacher = obj.session.teacher
        return teacher.get_full_name() if hasattr(teacher, "get_full_name") else str(teacher)

    session_teacher.short_description = "Преподаватель"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == ROLE_ADMIN:
            return qs.filter(user__organization_id=request.user.organization_id)
        return qs.none()
