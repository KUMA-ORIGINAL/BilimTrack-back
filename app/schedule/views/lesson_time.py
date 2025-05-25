from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins

from schedule.models import LessonTime
from schedule.serializers import LessonTimeSerializer


@extend_schema(tags=['schedule'])
class LessonTimeViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin):
    """
    ViewSet для получения списка времён занятий.
    """
    queryset = LessonTime.objects.all()
    serializer_class = LessonTimeSerializer
