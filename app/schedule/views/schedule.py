import datetime
from datetime import date

from django.db import models
from django.db.models import Min, Max
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from schedule.models import Schedule
from schedule.serializers import ScheduleCreateUpdateSerializer, ScheduleSerializer, MentorScheduleSerializer


@extend_schema(tags=['schedule'])
class ScheduleViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = [
        'education_level',
        'groups', 'teacher', 'subject', 'room',
        'day_of_week', 'lesson_time', 'lesson_type'
    ]
    search_fields = [
        'teacher__full_name',
        'subject__name', 'room__number'
    ]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ScheduleCreateUpdateSerializer
        return ScheduleSerializer

    def get_queryset(self):
        queryset = Schedule.objects.select_related(
            'subject', 'teacher', 'room', 'lesson_time'
        ).prefetch_related('groups').all()
        user = self.request.user

        if getattr(user, "organization_id", None):
            queryset = queryset.filter(organization=user.organization)

        return queryset

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


def get_week_type(date=None):
    if date is None:
        date = datetime.date.today()
    week_of_month = (date.day - 1) // 7 + 1
    return "top" if week_of_month % 2 == 1 else "bottom"


@extend_schema(tags=['schedule'])
class MentorScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mentor = request.user

        # Получаем текущий тип недели
        current_week_type = get_week_type()

        # Получаем все пары текущего ментора с учётом недели
        qs = Schedule.objects.filter(teacher=mentor).filter(
            # или "без деления", или текущая неделя
            models.Q(week_type="weekly") | models.Q(week_type=current_week_type)
        ).select_related(
            "lesson_time", "room", "subject"
        ).order_by("day_of_week", "lesson_time__start_time")

        serializer = MentorScheduleSerializer(qs, many=True)

        total_classes = qs.count()
        total_minutes = sum(
            (s.lesson_time.end_time.hour * 60 + s.lesson_time.end_time.minute) -
            (s.lesson_time.start_time.hour * 60 + s.lesson_time.start_time.minute)
            for s in qs
        )
        total_hours = round(total_minutes / 60, 1)

        # ---- Время за сегодня ----
        today = datetime.date.today().weekday()  # 0 = понедельник
        today_qs = qs.filter(day_of_week=today)

        day_start = today_qs.aggregate(start=Min("lesson_time__start_time"))["start"]
        day_end = today_qs.aggregate(end=Max("lesson_time__end_time"))["end"]

        return Response({
            "week_type": current_week_type,   # <--- чтобы фронт знал какая сейчас неделя
            "stats": {
                "total_classes": total_classes,
                "total_hours": total_hours,
                "today_start": day_start.strftime("%H:%M") if day_start else None,
                "today_end": day_end.strftime("%H:%M") if day_end else None,
            },
            "days": self.group_by_day(serializer.data),
        })

    def group_by_day(self, lessons):
        days = {str(d): [] for d in range(7)}
        for lesson in lessons:
            days[str(lesson["day_of_week"])].append(lesson)
        return days
