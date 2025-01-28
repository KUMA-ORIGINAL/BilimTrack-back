from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Group
from ..serializers import GroupSerializer


@extend_schema(tags=['Group'])
class GroupViewSet(viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def me(self, request):
        user = request.user
        group = user.group
        if not group:
            return Response({"detail": "User is not assigned to any group."},
                            status=status.HTTP_400_BAD_REQUEST)
        group_serializer = self.get_serializer(group)
        return Response(group_serializer.data)
