from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins

from schedule.models import LessonType
from schedule.serializers import LessonTypeSerializer


@extend_schema(tags=['schedule'])
class LessonTypeViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,):
    """
    ViewSet для получения списка типов занятий.
    """
    queryset = LessonType.objects.all()
    serializer_class = LessonTypeSerializer
