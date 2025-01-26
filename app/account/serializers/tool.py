from rest_framework import serializers

from account.models import Tool


class ToolSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tool
        fields = ('name', 'description', 'logo')
