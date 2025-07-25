from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, filters, mixins

from schedule.models import Schedule
from schedule.serializers import ScheduleCreateUpdateSerializer, ScheduleSerializer


@extend_schema(tags=['schedule'])
class ScheduleViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = Schedule.objects.select_related(
        'subject', 'teacher', 'room', 'lesson_time'
    ).prefetch_related('groups').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = [
        'groups', 'teacher', 'subject', 'room',
        'day_of_week', 'lesson_time', 'lesson_type'
    ]
    search_fields = [
        'teacher__full_name',
        'subject__name', 'room__number'
    ]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ScheduleCreateUpdateSerializer
        return ScheduleSerializer
