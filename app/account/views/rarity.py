from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins
from ..models import Rarity
from ..serializers import RaritySerializer


@extend_schema(tags=['Achievement and Rarity'])
class RarityViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = Rarity.objects.all()
    serializer_class = RaritySerializer