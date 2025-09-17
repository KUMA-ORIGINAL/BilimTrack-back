from rest_framework import serializers
from ..models import Session


class SessionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'topic')
        read_only_fields = ('id',)


class SessionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = [
            "id",
            "subject",
            "groups",
            "date",
            "start_time",
            "end_time",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not request.user:
            raise serializers.ValidationError("Нет текущего пользователя")

        groups = validated_data.pop("groups", [])

        session = Session.objects.create(
            teacher=request.user,
            **validated_data
        )
        session.groups.set(groups)
        return session
