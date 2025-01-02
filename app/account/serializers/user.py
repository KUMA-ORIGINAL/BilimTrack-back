from djoser.serializers import UserSerializer
from rest_framework import serializers

from .achievement_and_rarity import AchievementSerializer


class UserSerializer(UserSerializer):
    achievements = AchievementSerializer(many=True)
    group = serializers.StringRelatedField()

    class Meta(UserSerializer.Meta):
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'photo', 'role', 'group', 'achievements_count', 'points', 'rating',
                  'achievements',)
