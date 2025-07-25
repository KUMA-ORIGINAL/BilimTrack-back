from rest_framework import serializers

from ..models import Schedule
from .group import GroupSerializer
from .subject import SubjectSerializer
from .room import RoomSerializer
from .teacher import TeacherSerializer
from .lesson_time import LessonTimeSerializer
from .lesson_type import LessonTypeSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    subject = SubjectSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    lesson_time = LessonTimeSerializer(read_only=True)
    lesson_type = LessonTypeSerializer(read_only=True)

    class Meta:
        model = Schedule
        fields = [
            'id',
            'groups',
            'subject',
            'teacher',
            'room',
            'lesson_time',
            'lesson_type',
            'day_of_week',
            "week_type",
        ]


class ScheduleCreateUpdateSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        queryset=GroupSerializer.Meta.model.objects.all(),
        many=True
    )

    class Meta:
        model = Schedule
        fields = [
            'id',
            'groups',
            'subject',
            'teacher',
            'room',
            'lesson_time',
            'lesson_type',
            'day_of_week',
            "week_type",
        ]
