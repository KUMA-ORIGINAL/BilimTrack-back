from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, permissions, mixins, generics
from rest_framework.response import Response

from ..models import Grade, Session
from ..permissions import IsMentorOrReadOnly
from ..serializers import GradeSerializer, StudentGradeSerializer, GradeCreateSerializer

User = get_user_model()


@extend_schema(
    tags=['Grade Mentor'],
)
@extend_schema_view(
    list=extend_schema(
        summary='Получить оценки студентов по subject id',
        parameters = [
            OpenApiParameter(
                name='subject_id',
                description='ID of the subject for filtering grades',
                required=False,
                type=OpenApiTypes.INT,  # Тип параметра - целое число
                location=OpenApiParameter.QUERY  # Указание того, что параметр находится в строке запроса
            ),
            OpenApiParameter(
                name='group_id',
                description='ID of the group for filtering grades',
                required=False,
                type=OpenApiTypes.INT,  # Тип параметра - целое число
                location=OpenApiParameter.QUERY  # Указание того, что параметр находится в строке запроса
            )
        ]
    ),
)
class GradeMentorViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin):
    serializer_class = StudentGradeSerializer
    permission_classes = [IsMentorOrReadOnly]

    def list(self, request, *args, **kwargs):
        group_id = request.query_params.get('group_id')
        subject_id = request.query_params.get('subject_id')
        if not group_id or not subject_id:
            return Response({"error": "group_id and subject_id are required"}, status=400)

        users = User.objects.filter(group_id=group_id)
        sessions = Session.objects.filter(subject_id=subject_id).values_list('id', flat=True)

        user_grades_data = []
        for user in users:
            grades = Grade.objects.filter(user=user, session_id__in=sessions)
            user_grades_data.append({
                'user': user,
                'scores': grades
            })

        serializer = self.get_serializer(user_grades_data, many=True)
        return Response(serializer.data)


@extend_schema(
    tags=['Grade Mentor'],
)
@extend_schema_view(
    create=extend_schema(
        summary='Создание оценки для студента'
    ),
    update=extend_schema(
        summary='Изменение оценки для студента'
    ),
    partial_update=extend_schema(
        summary='Частичное изменение оценки для студента'
    ),
)
class GradeMentor2ViewSet(viewsets.GenericViewSet,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin):
    permission_classes = [IsMentorOrReadOnly]

    def get_queryset(self):
        return Grade.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return GradeCreateSerializer
        return GradeSerializer


@extend_schema(
    tags=['Grade student me'],
    parameters = [
        OpenApiParameter(
            name='subject_id',
            description='ID of the subject for filtering grades',
            required=False,
            type=OpenApiTypes.INT,  # Тип параметра - целое число
            location=OpenApiParameter.QUERY  # Указание того, что параметр находится в строке запроса
        )
    ]
)
class StudentGradeAPIView(generics.RetrieveAPIView):
    serializer_class = StudentGradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        subject_id = int(request.query_params.get('subject_id'))
        grades = Grade.objects.filter(user=user, subject_id=subject_id)
        data = {
            'user': user,
            'scores': grades
        }
        serializer = self.get_serializer(data)
        return Response(serializer.data)