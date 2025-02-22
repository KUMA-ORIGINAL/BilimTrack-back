from rest_framework import serializers

from .rarity import RaritySerializer
from ..models import Achievement, UserAchievement


class AchievementSerializer(serializers.ModelSerializer):
    rarity = RaritySerializer()

    class Meta:
        model = Achievement
        fields = ('id', 'name', 'description', 'photo', 'rarity', 'created_at')



class AchievementMeSerializer(serializers.ModelSerializer):
    rarity = RaritySerializer()
    is_opened = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = ('id', 'name', 'description', 'photo', 'rarity', 'created_at', 'is_opened')

    def get_is_opened(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                user_achievement = UserAchievement.objects.get(user=user, achievement=obj)
                return user_achievement.is_opened
            except UserAchievement.DoesNotExist:
                return False
        return False