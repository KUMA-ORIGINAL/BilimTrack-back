from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Payment

User = get_user_model()


class AbsencePaymentCreateRequestSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            "id",
            "payment_link",
        )
        read_only_fields = fields
