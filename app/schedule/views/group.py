from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from academics.models import Group
from schedule.models import Schedule
from schedule.serializers import GroupSerializer, GroupDetailSerializer, \
    ScheduleShortSerializer, GroupWithScheduleSerializer


@extend_schema(tags=['schedule'])
class GroupViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,):
    """
    ViewSet для получения списка учебных групп.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @extend_schema(
        responses=GroupWithScheduleSerializer,
        tags=['schedule']
    )
    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        group = self.get_object()
        schedule_qs = Schedule.objects.filter(groups=group).select_related(
            'subject', 'teacher', 'room', 'lesson_time'
        ).prefetch_related('groups')

        data = {
            'group': GroupDetailSerializer(group).data,
            'schedule': ScheduleShortSerializer(schedule_qs, many=True).data,
        }
        return Response(data)
