from collections import defaultdict

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, permissions, mixins, generics
from rest_framework.response import Response

from ..models import Grade
from ..permissions import IsMentorOrReadOnly
from ..serializers import GradeSerializer, StudentGradeSerializer


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
class GradeMentorViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin):
    serializer_class = GradeSerializer
    permission_classes = [IsMentorOrReadOnly]

    def get_queryset(self):
        # Получаем пользователей, отфильтрованных по groupId
        group_id = self.request.query_params.get('group_id')
        if group_id:
            return User.objects.filter(group_id=group_id)
        return User.objects.all()

    def get_serializer_class(self):
        # Используем разный сериализатор в зависимости от действия
        if self.action in ('create', 'update', 'partial_update'):
            return GradeSerializer
        return StudentGradeSerializer

    def list(self, request, *args, **kwargs):
        # Получаем пользователей
        users = self.get_queryset()

        # Получаем subjectId из параметров запроса
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response({"error": "subjectId is required"}, status=400)

        # Преобразуем subjectId в целое число
        subject_id = int(subject_id)

        # Собираем оценки для каждого пользователя
        user_grades_data = []
        for user in users:
            grades = Grade.objects.filter(user=user, subject_id=subject_id)
            user_grades_data.append({
                'user': user,
                'scores': grades
            })

        # Сериализуем данные и возвращаем ответ
        serializer = self.get_serializer(user_grades_data, many=True)
        return Response(serializer.data)

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