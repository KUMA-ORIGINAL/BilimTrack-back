from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Subject
from ..serializers import SubjectSerializer, SubjectListSerializer


@extend_schema(tags=['Subject'])
class SubjectViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return SubjectListSerializer
        return SubjectSerializer

    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def me(self, request):
        user = request.user
        group = user.group
        if not group:
            return Response({"detail": "User is not assigned to any group."},
                            status=status.HTTP_400_BAD_REQUEST)
        subjects = group.subjects.all()
        subjects_serializer = self.get_serializer(subjects, many=True)
        return Response(subjects_serializer.data)
