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
    summary="Создать или удалить занятие",
    description="Позволяет ментору создать новое занятие (POST) или удалить своё занятие (DELETE)."
)
class SessionCreateDeleteView(generics.CreateAPIView,
                              generics.DestroyAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    http_method_names = ['post', 'delete']

    def get_queryset(self):
        """Разрешаем удалять только свои занятия"""
        qs = super().get_queryset()
        if self.request.user.role == 'mentor':
            return qs.filter(teacher=self.request.user)
        return qs.none()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()