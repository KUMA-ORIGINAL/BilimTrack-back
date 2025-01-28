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


@extend_schema(tags=['Grade Mentor'])
@extend_schema_view(
    list=extend_schema(
        summary='Получить оценки студентов по subject id'
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
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsMentorOrReadOnly]
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['subject_id']


@extend_schema(
    tags=['Grade student me'],
    parameters = [
        OpenApiParameter(
            name='subjectId',
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