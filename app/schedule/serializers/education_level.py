from rest_framework import serializers
from academics.models import EducationLevel


class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = ['id', 'name']
