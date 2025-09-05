from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Group, Subject, GroupSubjectMentor
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

    @action(detail=False, methods=['get'], url_path='mentor/me', url_name='mentor-me')
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

        # ⚡ правильная фильтрация через ManyToMany 'subjects'
        group_ids = GroupSubjectMentor.objects.filter(
            subjects=subject,
            mentor=request.user
        ).values_list('group_id', flat=True)

        groups = Group.objects.filter(id__in=group_ids)

        if not groups.exists():
            return Response({"detail": "You are not a mentor in any group for this subject."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)
