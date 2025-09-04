from django.contrib import admin
from unfold.admin import TabularInline

from account.models import ROLE_ADMIN
from common.admin import BaseModelAdmin
from ..models import Organization, EducationLevel


class EducationLevelInline(TabularInline):
    model = EducationLevel
    extra = 1
    fields = ("name",)
    show_change_link = True


@admin.register(Organization)
class OrganizationAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'detail_link')
    search_fields = ('name',)
    inlines = [EducationLevelInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == ROLE_ADMIN:
            return qs.filter(id=request.user.organization_id)
        return qs.none()
