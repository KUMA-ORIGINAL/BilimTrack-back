from django_filters.rest_framework import DjangoFilterBackend
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
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['organization', ]

    def get_queryset(self):
        queryset = User.objects.filter(role='mentor')
        user = self.request.user

        if getattr(user, "organization_id", None):
            queryset = queryset.filter(organization=user.organization)

        return queryset

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
