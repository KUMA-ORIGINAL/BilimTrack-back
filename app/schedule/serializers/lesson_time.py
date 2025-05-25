from rest_framework import serializers
from ..models import LessonTime


class LessonTimeSerializer(serializers.ModelSerializer):
    startTime = serializers.TimeField(source='start_time', format='%H:%M')
    endTime = serializers.TimeField(source='end_time', format='%H:%M')

    class Meta:
        model = LessonTime
        fields = ['id', 'startTime', 'endTime']
