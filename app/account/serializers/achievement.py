from rest_framework import serializers

from .rarity import RaritySerializer
from ..models import Achievement


class AchievementSerializer(serializers.ModelSerializer):
    rarity = RaritySerializer()

    class Meta:
        model = Achievement
        fields = ('id', 'name', 'description', 'photo', 'rarity', 'created_at')
