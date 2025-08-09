from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from account.models import User
from schedule.models import Schedule
from schedule.serializers import TeacherSerializer, TeacherWithScheduleSerializer, ScheduleTeacherShortSerializer


@extend_schema(tags=['schedule'])
class TeacherViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    """
    ViewSet для получения списка преподавателей (роль mentor).
    """
    serializer_class = TeacherSerializer

    def get_queryset(self):
        return User.objects.filter(role='mentor')

    @extend_schema(
        responses=TeacherWithScheduleSerializer,
        tags=['schedule']
    )
    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        teacher = self.get_object()
        schedule_qs = Schedule.objects.filter(teacher=teacher).select_related(
            'subject', 'room', 'lesson_time'
        ).prefetch_related('groups').order_by('lesson_time__start_time')
        data = {
            'teacher': TeacherSerializer(teacher).data,
            'schedule': ScheduleTeacherShortSerializer(schedule_qs, many=True).data,
        }
        return Response(data)
