from rest_framework import serializers
from academics.models import Group
from schedule.serializers import CourseSerializer


class GroupSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'course']
