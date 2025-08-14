from rest_framework import serializers
from ..models import Session


class SessionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'topic')
        read_only_fields = ('id',)