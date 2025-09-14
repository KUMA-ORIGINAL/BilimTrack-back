from django.contrib import admin, messages
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from unfold.contrib.filters.admin import RelatedDropdownFilter
from unfold.decorators import action

from account.models import ROLE_ADMIN
from common.admin import BaseModelAdmin
from schedule.models import Schedule
from ..models import Teaching


@admin.register(Teaching)
class TeachingAdmin(BaseModelAdmin):
    list_display = ('id', 'mentor', 'group', 'subject', 'detail_link')
    list_display_links = ('id',)
    list_filter = (
        ('mentor', RelatedDropdownFilter),
        ('group', RelatedDropdownFilter),
        ('subject', RelatedDropdownFilter)
    )
    list_filter_submit = True
    search_fields = (
        'mentor__username',
        'mentor__first_name',
        'mentor__last_name',
        'group__name',
        'subject__name',
    )
    autocomplete_fields = ('mentor', 'group', 'subject')
    list_select_related = ('mentor', 'group', 'subject')

    actions_list = ["generate_from_schedule"]

    @action(
        description="Сгенерировать связки из расписания",
        url_path="generate_from_schedule",
        permissions=['generate_from_schedule']
    )
    def generate_from_schedule(self, request):
        # Базовый queryset расписаний
        qs = Schedule.objects.prefetch_related("groups")

        # Ограничиваем расписания по организации
        if not request.user.is_superuser and getattr(request.user, "role", None) == ROLE_ADMIN:
            qs = qs.filter(organization_id=request.user.organization_id)

        # Собираем все потенциальные Teaching (mentor, subject, group)
        new_teachings = []
        for schedule in qs:
            for group in schedule.groups.all():
                new_teachings.append((schedule.teacher_id, schedule.subject_id, group.id))

        if not new_teachings:
            self.message_user(request, f"⚠️ Подходящих расписаний не найдено", level=messages.WARNING)
            return redirect(reverse_lazy("admin:academics_teaching_changelist"))

        # Чтобы убрать дубли в new_teachings → set()
        new_teachings = set(new_teachings)

        # Уже существующие связки
        existing = set(
            Teaching.objects.filter(
                mentor_id__in=[t[0] for t in new_teachings],
                subject_id__in=[t[1] for t in new_teachings],
                group_id__in=[t[2] for t in new_teachings],
            ).values_list("mentor_id", "subject_id", "group_id")
        )

        # Находим отсутствующие
        to_create = [
            Teaching(mentor_id=m, subject_id=s, group_id=g)
            for (m, s, g) in new_teachings
            if (m, s, g) not in existing
        ]

        with transaction.atomic():
            Teaching.objects.bulk_create(to_create, ignore_conflicts=True)

        created_count = len(to_create)

        # Сообщение пользователю
        if created_count > 0:
            self.message_user(
                request,
                f"✅ Создано {created_count} новых связок преподавания",
                level=messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                f"⚠️ Новых связок преподавания не найдено",
                level=messages.WARNING
            )

        return redirect(reverse_lazy("admin:academics_teaching_changelist"))

    def has_generate_from_schedule_permission(self, request, obj=None):
        return request.user.role == ROLE_ADMIN

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == ROLE_ADMIN:
            return qs.filter(group__organization_id=request.user.organization_id)
        return qs.none()
