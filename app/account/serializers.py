from djoser.serializers import UserSerializer


class UserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'photo', 'role',)
