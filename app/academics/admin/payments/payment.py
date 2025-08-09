from django.contrib import admin

from academics.models import Payment
from common.admin import BaseModelAdmin


@admin.register(Payment)
class PaymentAdmin(BaseModelAdmin):
    list_display = ("id", "user", "grade", "amount", "status", "paid_at", "created_at", 'detail_link')
    list_filter = ("status", "created_at")
    search_fields = ("id", "user__username", "user__first_name", "user__last_name")
    readonly_fields = ("created_at", "updated_at", "paid_at", "payment_link", "provider_payload")
