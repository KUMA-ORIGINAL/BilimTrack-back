from rest_framework import serializers
from academics.models import Group
from .course import CourseSerializer


class GroupSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'course', 'education_level']


class GroupDetailSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    curator_name = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'course', 'curator_name']

    def get_curator_name(self, obj):
        if obj.curator:
            return f"{obj.curator.last_name} {obj.curator.first_name[0].upper()}."
        return None