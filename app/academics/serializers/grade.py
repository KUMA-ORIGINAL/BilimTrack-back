from django.contrib.auth import get_user_model
from rest_framework import serializers

from .lesson_topic import LessonTopicShortSerializer
from ..models import Grade, Session, Payment

User = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'username')


class GradeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('id', 'grade')


class GradeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = ('id', 'session', 'grade', 'user')


class GradeShortSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source='session.date', format='%d-%m-%Y')
    session_id = serializers.UUIDField(source='session.id')
    requires_payment = serializers.SerializerMethodField()
    can_submit_make_up = serializers.SerializerMethodField()

    class Meta:
        model = Grade
        fields = ('id', 'grade', 'date', 'session_id', 'requires_payment', 'can_submit_make_up')

    def get_requires_payment(self, obj):
        return obj.grade == 0

    def get_can_submit_make_up(self, obj):
        return Payment.objects.filter(user=obj.user, grade=obj, status=Payment.Status.PAID).exists()


class SessionShortSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format='%d-%m-%Y')
    topic = LessonTopicShortSerializer()

    class Meta:
        model = Session
        fields = ('id', 'date', 'topic')


class GradeListSerializer(serializers.Serializer):
    user = UserShortSerializer(read_only=True)
    scores = GradeShortSerializer(many=True)


class SessionAndGradeSerializer(serializers.Serializer):
    sessions = SessionShortSerializer(many=True)
    grades = GradeListSerializer(many=True)


class AttendanceMarkSerializer(serializers.ModelSerializer):
    session_id = serializers.UUIDField(source='session.id', read_only=True)
    date = serializers.DateField(source='session.date', format='%d-%m-%Y', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Grade
        fields = ('id', 'session_id', 'user_id', 'grade', 'date')


class AttendanceMarkRequestSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()


class MakeUpSubmissionRequestSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    make_up_link = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    make_up_file = serializers.FileField(required=False, allow_null=True)

    def validate(self, attrs):
        if not attrs.get('make_up_link') and not attrs.get('make_up_file'):
            raise serializers.ValidationError("Нужно указать make_up_link или приложить make_up_file.")
        return attrs
