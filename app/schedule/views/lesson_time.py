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
    serializer_class = LessonTimeSerializer

    def get_queryset(self):
        queryset = LessonTime.objects.all()
        user = self.request.user

        if getattr(user, "organization_id", None):
            queryset = queryset.filter(organization=user.organization)

        return queryset