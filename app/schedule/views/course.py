from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins

from academics.models import Course
from ..serializers import CourseSerializer


@extend_schema(tags=['schedule'])
class CourseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_fields = ['organization', 'number']
    search_fields = ['number', 'organization__name']
    ordering_fields = ['number', 'organization']
