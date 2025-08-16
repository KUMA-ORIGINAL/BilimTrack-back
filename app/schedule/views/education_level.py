from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins

from academics.models import EducationLevel
from ..serializers import EducationLevelSerializer


@extend_schema(tags=['schedule'])
class EducationLevelViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin):
    """
    ViewSet для получения списка уровней образования.
    """
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer
