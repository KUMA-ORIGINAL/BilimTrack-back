from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins
from ..models import Rarity, Achievement
from ..serializers import RaritySerializer, AchievementSerializer


@extend_schema(tags=['Achievement and Rarity'])
class RarityViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = Rarity.objects.all()
    serializer_class = RaritySerializer


@extend_schema(tags=['Achievement and Rarity'])
class AchievementViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer