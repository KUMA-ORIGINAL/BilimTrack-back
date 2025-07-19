from rest_framework import serializers
from account.models import Education


class EducationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Education
        fields = [
            'id',
            'user',
            'institution',
            'field_of_study',
            'date',
            'description',
        ]
        extra_kwargs = {
            'institution': {'required': True},
            'field_of_study': {'required': False, 'allow_null': True, 'allow_blank': True},
            'date': {'required': True},
            'description': {'required': False, 'allow_null': True, 'allow_blank': True},
        }
