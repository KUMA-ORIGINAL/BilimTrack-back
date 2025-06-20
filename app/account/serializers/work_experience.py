from rest_framework import serializers

from account.models import WorkExperience


class WorkExperienceSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = WorkExperience
        fields = [
            'id',
            'user',
            'position',
            'company',
            'start_date',
            'end_date',
            'description',
        ]
        extra_kwargs = {
            'position': {'required': False},
            'company': {'required': False},
            'start_date': {'required': False},
            'end_date': {'required': False, 'allow_null': True},
            'description': {'required': False, 'allow_blank': True},
        }
