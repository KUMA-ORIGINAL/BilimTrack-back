from rest_framework import serializers

from schedule.models import LessonType


class LessonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonType
        fields = ['id', 'name']
