from rest_framework import serializers

from ..models import Subject, Group


class SubjectSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField()  # Отображение имени группы
    photo = serializers.ImageField()


    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'photo', 'group', 'created_at', 'makalabox_url']

class GroupSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'rules', 'contract', 'created_at', 'subjects']


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'points']


class SubjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'photo',]
