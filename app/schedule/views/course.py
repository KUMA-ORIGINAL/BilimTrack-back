from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins

from academics.models import Course
from ..serializers import CourseSerializer


@extend_schema(tags=['schedule'])
class CourseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['education_level', 'organization']

    def get_queryset(self):
        queryset = Course.objects.all()
        user = self.request.user

        if getattr(user, "organization_id", None):
            queryset = queryset.filter(organization=user.organization)

        return queryset
