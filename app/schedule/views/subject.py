from django_filters.rest_framework import DjangoFilterBackend
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
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['education_level', 'organization']

    def get_queryset(self):
        queryset = Subject.objects.all()
        user = self.request.user

        if getattr(user, "organization_id", None):
            queryset = queryset.filter(organization=user.organization)

        return queryset
