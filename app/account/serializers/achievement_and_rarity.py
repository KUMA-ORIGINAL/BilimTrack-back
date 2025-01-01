from rest_framework import serializers

from ..models import Rarity, Achievement


class RaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Rarity
        fields = ('id', 'name')

class AchievementSerializer(serializers.ModelSerializer):
    rarity = RaritySerializer()

    class Meta:
        model = Achievement
        fields = ('id', 'name', 'description', 'photo', 'rarity', 'created_at')
