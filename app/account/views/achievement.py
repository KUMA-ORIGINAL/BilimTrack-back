from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins
from ..models import Achievement
from ..serializers import AchievementSerializer


@extend_schema(tags=['Achievement and Rarity'])
class AchievementViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
