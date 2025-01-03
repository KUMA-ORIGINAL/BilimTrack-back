from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, mixins, permissions, generics

from ..serializers import UserListSerializer, MeSerializer, MeUpdateSerializer

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


@extend_schema(tags=['Users'])
@extend_schema_view(
    list=extend_schema(summary='Получение студентов отсортированных по баллам')
)
class UserViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin):
    serializer_class = UserListSerializer
    queryset = User.objects.filter(role='student').order_by('-points')
    permission_classes = [permissions.IsAuthenticated]

