from rest_framework import serializers

from ..models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField()  # Отображение имени группы
    photo = serializers.ImageField()


    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'photo', 'group', 'created_at', 'makalabox_url']


class SubjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'photo',]
