from rest_framework import serializers
from ..models import LessonTopic


class LessonTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonTopic
        fields = ('id', 'subject', 'title')

    def create(self, validated_data):
        """
        Автоматически подставляем current_user в mentor.
        """
        validated_data['mentor'] = self.context['request'].user
        return super().create(validated_data)


class LessonTopicShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonTopic
        fields = ["id", "title"]