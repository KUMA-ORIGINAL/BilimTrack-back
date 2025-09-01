from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins

from academics.models import EducationLevel
from ..serializers import EducationLevelSerializer


@extend_schema(tags=['schedule'])
class EducationLevelViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin):
    """
    ViewSet для получения списка уровней образования.
    Фильтрация по organization пользователя.
    """
    serializer_class = EducationLevelSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['organization', ]

    def get_queryset(self):
        queryset = EducationLevel.objects.all()
        user = self.request.user

        if getattr(user, "organization_id", None):
            queryset = queryset.filter(organization=user.organization)

        return queryset
