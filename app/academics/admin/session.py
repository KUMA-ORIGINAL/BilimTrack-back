import datetime
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from unfold.decorators import display, action

from account.models import ROLE_ADMIN
from common.admin import BaseModelAdmin
from ..models import Session
from ..services.sessions import generate_sessions_for_date


@admin.register(Session)
class SessionAdmin(BaseModelAdmin):
    list_display = ('id', 'subject', 'date', 'display_time', 'is_active', 'detail_link')
    list_display_links = ('id', 'subject')
    search_fields = ('subject__name',)
    list_filter = ('subject', 'is_active', 'date', 'teacher__organization')
    date_hierarchy = 'date'
    autocomplete_fields = ('groups', 'teacher', 'subject', 'topic', 'room')

    # --- красивый вывод времени
    @display(description=_("Время занятия"))
    def display_time(self, obj):
        return f"{obj.start_time.strftime('%H:%M')} - {obj.end_time.strftime('%H:%M')}"

    # --- универсальный метод генерации
    def _generate_and_notify(self, request, target_date: datetime.date, label: str):
        created_count = generate_sessions_for_date(target_date)
        if created_count > 0:
            self.message_user(
                request,
                _(f"✅ Создано {created_count} занятий на {label} ({target_date})"),
                level=messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                _(f"⚠️ Новых занятий на {label} ({target_date}) не создано"),
                level=messages.WARNING
            )
        return redirect(reverse_lazy("admin:academics_session_changelist"))

    # --- экшены
    actions_list = ["generate_today_sessions_action", "generate_tomorrow_sessions_action"]

    @action(
        description=_("Создать занятия на сегодня"),
        url_path="generate-today-sessions",
        permissions=["add"]
    )
    def generate_today_sessions_action(self, request):
        today = datetime.date.today()
        return self._generate_and_notify(request, today, _("сегодня"))

    @action(
        description=_("Создать занятия на завтра"),
        url_path="generate-tomorrow-sessions",
        permissions=["add"]
    )
    def generate_tomorrow_sessions_action(self, request):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        return self._generate_and_notify(request, tomorrow, _("завтра"))

    # --- права доступа
    def has_generate_today_sessions_permission(self, request):
        return request.user.is_superuser or request.user.has_perm("academics.add_session")

    def has_generate_tomorrow_sessions_permission(self, request):
        return self.has_generate_today_sessions_permission(request)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == ROLE_ADMIN:
            return qs.filter(subject__organization_id=request.user.organization_id)
        return qs.none()
