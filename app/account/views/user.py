from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, generics
from rest_framework.generics import get_object_or_404

from ..serializers import MeSerializer, MeUpdateSerializer

User = get_user_model()

@extend_schema(tags=['Users Me'])
class MeViewSet(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes  = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return MeUpdateSerializer
        return MeSerializer

    def get_object(self):
        return self.request.user

@extend_schema(tags=['Users'], summary='Получение профиля пользователя по username')
class UserViewSet(generics.RetrieveAPIView):
    serializer_class = MeSerializer

    def get_object(self):
        """Возвращает объект пользователя по его username"""
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)
