from rest_framework import serializers
from account.models import User


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name']
