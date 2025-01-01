from djoser.serializers import UserSerializer

from .achievement_and_rarity import AchievementSerializer


class UserSerializer(UserSerializer):
    achievements = AchievementSerializer(many=True)

    class Meta(UserSerializer.Meta):
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'photo', 'role', 'achievements')
