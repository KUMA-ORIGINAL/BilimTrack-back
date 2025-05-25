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
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
