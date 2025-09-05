from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from ..models import Session
from ..serializers import SessionUpdateSerializer, SessionCreateSerializer


@extend_schema(
    tags=["Mentor"],
    summary="Изменить тему урока в сессии",
    description="Позволяет ментору изменить только поле 'topic' у занятия (PATCH)."
)
class SessionUpdateView(generics.UpdateAPIView,
                        generics.CreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]  # можно сделать кастомный IsMentor

    http_method_names = ['patch']


@extend_schema(
    tags=["Mentor"],
    summary="Создать занятие",
    description="Позволяет ментору создать новое занятие (POST)."
)
class SessionCreateView(generics.CreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    http_method_names = ['post']
