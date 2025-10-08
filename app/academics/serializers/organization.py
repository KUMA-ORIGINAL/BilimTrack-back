from rest_framework import serializers
from ..models import Organization


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "logo",
            "website",
            "news_api",
            "events_api",
            "latitude",
            "longitude",
            "radius_meters",
        ]
