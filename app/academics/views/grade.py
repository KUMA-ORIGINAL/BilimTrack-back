from collections import defaultdict

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, mixins, generics
from rest_framework.response import Response

from ..models import Grade
from ..permissions import IsMentorOrReadOnly
from ..serializers import GradeSerializer, StudentGradeSerializer


@extend_schema(tags=['Grade Mentor'])
class GradeMentorViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsMentorOrReadOnly]
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['subject_id']


@extend_schema(tags=['Grade student me'])
class GradeStudentAPIView(generics.ListAPIView):
    queryset = Grade.objects.all()
    serializer_class = StudentGradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subject_id']

    def get_queryset(self):
        # Отфильтровываем оценки только для текущего пользователя
        return Grade.objects.filter(user=self.request.user)
