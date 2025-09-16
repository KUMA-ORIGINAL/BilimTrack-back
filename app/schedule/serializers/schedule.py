from rest_framework import serializers

from ..models import Schedule
from .group import GroupSerializer, GroupDetailSerializer
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
            'education_level'
        ]


class ScheduleGroupShortSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    lesson_time = LessonTimeSerializer(read_only=True)
    lesson_type = LessonTypeSerializer(read_only=True)

    class Meta:
        model = Schedule
        fields = [
            'id',
            'subject',
            'teacher',
            'room',
            'lesson_time',
            'lesson_type',
            'day_of_week',
            'week_type',
        ]


class ScheduleTeacherShortSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    subject = SubjectSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    lesson_time = LessonTimeSerializer(read_only=True)
    lesson_type = LessonTypeSerializer(read_only=True)

    class Meta:
        model = Schedule
        fields = [
            'id',
            'groups',
            'subject',
            'room',
            'lesson_time',
            'lesson_type',
            'day_of_week',
            'week_type',
        ]


class GroupWithScheduleSerializer(serializers.Serializer):
    group = GroupDetailSerializer()
    schedule = ScheduleGroupShortSerializer(many=True)
    week_type = serializers.CharField()


class TeacherWithScheduleSerializer(serializers.Serializer):
    teacher = TeacherSerializer()
    schedule = ScheduleTeacherShortSerializer(many=True)


class ScheduleCreateUpdateSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        queryset=GroupSerializer.Meta.model.objects.all(),
        many=True
    )

    class Meta:
        model = Schedule
        fields = [
            'id',
            'education_level',
            'groups',
            'subject',
            'teacher',
            'room',
            'lesson_time',
            'lesson_type',
            'day_of_week',
            "week_type",
        ]


class MentorScheduleSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    lesson_time = LessonTimeSerializer(read_only=True)
    lesson_type = LessonTypeSerializer(read_only=True)
    day_name = serializers.CharField(source="get_day_of_week_display", read_only=True)

    duration_minutes = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = [
            "id",
            "subject",
            "room",
            "lesson_type",
            "day_of_week",
            "day_name",
            "lesson_time",
            "duration_minutes",
        ]

    def get_duration_minutes(self, obj):
        start = obj.lesson_time.start_time
        end = obj.lesson_time.end_time
        return (end.hour * 60 + end.minute) - (start.hour * 60 + start.minute)
