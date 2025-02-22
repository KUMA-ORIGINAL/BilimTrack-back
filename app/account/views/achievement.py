from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Achievement
from ..serializers import AchievementSerializer, AchievementMeSerializer


@extend_schema(tags=['Achievement and Rarity'])
class AchievementViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer


@extend_schema(tags=['Achievement and Rarity'])
class AchievementMeViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin):
    queryset = Achievement.objects.all()
    serializer_class = AchievementMeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
