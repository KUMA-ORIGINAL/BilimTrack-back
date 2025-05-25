from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins

from account.models import User
from schedule.serializers import TeacherSerializer


@extend_schema(tags=['schedule'])
class TeacherViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    """
    ViewSet для получения списка преподавателей (роль mentor).
    """
    serializer_class = TeacherSerializer

    def get_queryset(self):
        return User.objects.filter(role='mentor')
