from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins

from schedule.models import Room
from schedule.serializers import RoomSerializer


@extend_schema(tags=['schedule'])
class RoomViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin):
    """
    ViewSet для получения списка аудиторий.
    """
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = Room.objects.all()
        user = self.request.user

        if getattr(user, "organization_id", None):
            queryset = queryset.filter(organization=user.organization)

        return queryset