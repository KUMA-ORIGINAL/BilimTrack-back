from django.contrib import admin

from academics.models import PaymentToken
from common.admin import BaseModelAdmin


@admin.register(PaymentToken)
class PaymentTokenAdmin(BaseModelAdmin):
    list_display = ("organization", "created_at", 'detail_link')
    search_fields = ("organization__name",)
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("organization",)
