from rest_framework import serializers

from ..models import Rarity


class RaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Rarity
        fields = ('id', 'name')