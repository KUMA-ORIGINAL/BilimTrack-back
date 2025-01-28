from rest_framework import serializers

from . import SubjectSerializer
from ..models import  Group


class GroupSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'rules', 'contract', 'created_at', 'subjects']


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'points']