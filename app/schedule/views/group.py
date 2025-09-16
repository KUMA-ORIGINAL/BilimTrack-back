from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from academics.models import Group
from schedule.models import Schedule
from schedule.serializers import GroupSerializer, GroupDetailSerializer, \
    ScheduleGroupShortSerializer, GroupWithScheduleSerializer
from schedule.utils import get_week_type


@extend_schema(tags=['schedule'])
class GroupViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,):
    """
    ViewSet для получения списка учебных групп.
    """
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['education_level', ]

    def get_queryset(self):
        queryset = Group.objects.all()
        user = self.request.user

        if getattr(user, "organization_id", None):
            queryset = queryset.filter(organization=user.organization)

        return queryset

    @extend_schema(
        responses=GroupWithScheduleSerializer,
        tags=['schedule']
    )
    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        group = self.get_object()
        schedule_qs = Schedule.objects.filter(groups=group).select_related(
            'subject', 'teacher', 'room', 'lesson_time'
        ).prefetch_related('groups').order_by('lesson_time__start_time')

        # Определяем какая неделя
        today_week_type = get_week_type()

        data = {
            'group': GroupDetailSerializer(group).data,
            'schedule': ScheduleGroupShortSerializer(schedule_qs, many=True).data,
            'week_type': today_week_type,  # просто добавили в ответ
        }
        return Response(data)
