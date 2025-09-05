from rest_framework import serializers

from ..models import Subject
from .course import CourseSerializer


class SubjectSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField()  # Отображение имени группы
    photo = serializers.ImageField()


    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'photo', 'group', 'created_at', 'makalabox_url']


class SubjectMentorSerializer(serializers.ModelSerializer):
    course = CourseSerializer(source="semester.course", read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'course',]


class SubjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'photo',]
