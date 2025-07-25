from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Group, Subject
from ..serializers import GroupSerializer, MentorGroupSerializer


@extend_schema(tags=['Group'])
@extend_schema_view(
    mentor_me=extend_schema(
        summary='Получение групп по id предмета для ментора',
        parameters = [
            OpenApiParameter(
                name='subject_id',
                description='ID of the subject for filtering grades',
                required=False,
                type=OpenApiTypes.INT,  # Тип параметра - целое число
                location=OpenApiParameter.QUERY  # Указание того, что параметр находится в строке запроса
            ),
        ]
    )
)
class GroupViewSet(viewsets.GenericViewSet):
    queryset = Group.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'me':
            return GroupSerializer
        return MentorGroupSerializer

    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def me(self, request):
        user = request.user
        group = user.group
        if not group:
            return Response({"detail": "User is not assigned to any group."},
                            status=status.HTTP_400_BAD_REQUEST)
        group_serializer = self.get_serializer(group)
        return Response(group_serializer.data)

    @action(detail=False, methods=['get'], url_path='mentor/me', url_name='me')
    def mentor_me(self, request):
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response({"detail": "Subject ID is required."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return Response({"detail": "Subject not found."},
                            status=status.HTTP_404_NOT_FOUND)

        groups = subject.groups.all()

        user_mentor_groups = request.user.mentor_groups.all()
        groups = groups.filter(id__in=user_mentor_groups.values_list('id', flat=True))

        if not groups.exists():
            return Response({"detail": "You are not a mentor in any group for this subject."},
                            status=status.HTTP_400_BAD_REQUEST)

        group_serializer = self.get_serializer(groups, many=True)
        return Response(group_serializer.data)
