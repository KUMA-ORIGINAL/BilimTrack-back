from rest_framework import serializers

from . import SubjectSerializer
from ..models import  Group


class GroupSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'created_at', 'subjects']


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'points']


class MentorGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']


class GroupShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']