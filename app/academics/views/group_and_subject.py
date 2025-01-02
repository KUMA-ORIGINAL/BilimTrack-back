from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Group, Subject
from ..serializers import GroupSerializer, SubjectSerializer

@extend_schema(tags=['Group and Subject'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить список групп отсортированных по баллам'
    ),
)
class GroupViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def me(self, request):
        user = request.user
        group = user.group
        if not group:
            return Response({"detail": "User is not assigned to any group."},
                            status=status.HTTP_400_BAD_REQUEST)
        # Предполагаем, что у пользователя только одна группа
        group_serializer = self.get_serializer(group)
        return Response(group_serializer.data)


@extend_schema(tags=['Group and Subject'])
class SubjectViewSet(viewsets.GenericViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

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
