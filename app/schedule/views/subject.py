from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins

from academics.models import Subject
from schedule.serializers import SubjectSerializer


@extend_schema(tags=['schedule'])
class SubjectViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    """
    ViewSet для получения списка предметов.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
