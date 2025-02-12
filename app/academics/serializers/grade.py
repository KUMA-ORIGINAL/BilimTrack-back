from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Grade

User = get_user_model()

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'username')


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('id', 'date', 'grade')


class GradeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('id', 'date', 'grade', 'user', 'subject')


class GradeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('id', 'date', 'grade')


class StudentGradeSerializer(serializers.Serializer):
    user = UserShortSerializer(read_only=True)
    scores = GradeShortSerializer(many=True)