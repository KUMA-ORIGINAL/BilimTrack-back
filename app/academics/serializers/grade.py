from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Grade, Session

User = get_user_model()


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'username')


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('id', 'grade')


class GradeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('id', 'grade', 'user')


class GradeShortSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source='session.date', format='%d-%m-%Y')
    session_id = serializers.UUIDField(source='session.id')

    class Meta:
        model = Grade
        fields = ('id', 'grade', 'date', 'session_id')


class SessionShortSerializer(serializers.ModelSerializer):
    sessionId = serializers.UUIDField(source='id')
    date = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Session
        fields = ('sessionId', 'date')


class StudentGradeSerializer(serializers.Serializer):
    user = UserShortSerializer(read_only=True)
    scores = GradeShortSerializer(many=True)


class AttendanceMarkSerializer(serializers.ModelSerializer):
    session_id = serializers.UUIDField(source='session.id', read_only=True)
    date = serializers.DateField(source='session.date', format='%d-%m-%Y', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Grade
        fields = ('id', 'session_id', 'user_id', 'grade', 'date')


class AttendanceMarkRequestSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()