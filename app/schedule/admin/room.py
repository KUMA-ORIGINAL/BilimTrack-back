from django.contrib import admin

from account.models import ROLE_ADMIN
from common.admin import BaseModelAdmin
from ..models import (
    Room,
)


@admin.register(Room)
class RoomAdmin(BaseModelAdmin):
    list_display_links = ('id', 'building', 'number')
    search_fields = ('building', 'number')

    def get_list_display(self, request):
        list_display = ("id", "building", "number", 'organization', 'detail_link')
        if request.user.role == ROLE_ADMIN:
            list_display = ("building", "number", 'detail_link')
        return list_display

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if request.user.is_superuser:
            return fields
        elif request.user.role == ROLE_ADMIN:
            return [field for field in fields if field not in ['organization',]]
        return fields

    def save_model(self, request, obj, form, change):
        if request.user.role == ROLE_ADMIN and not change:
            obj.organization_id = request.user.organization_id
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == ROLE_ADMIN:
            return qs.filter(organization_id=request.user.organization_id)
        return qs.none()
