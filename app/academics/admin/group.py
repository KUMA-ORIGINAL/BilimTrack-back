from django.contrib import admin

from account.models import ROLE_ADMIN
from common.admin import BaseModelAdmin
from ..models import Group, EducationLevel


@admin.register(Group)
class GroupAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'points', 'organization', 'education_level', 'detail_link')
    list_display_links = ('id', 'name',)
    list_filter = ('organization', 'education_level')
    search_fields = ('name',)
    autocomplete_fields = ('course', 'curator')

    def get_readonly_fields(self, request, obj=None):
        if request.user.role == ROLE_ADMIN:
            return ('points',)
        return ()

    def get_list_display(self, request):
        list_display = ('id', 'name', 'points', 'organization', 'education_level', 'detail_link')
        if request.user.role == ROLE_ADMIN:
            list_display = ('name', 'points', 'education_level', 'detail_link')
        return list_display

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if request.user.is_superuser:
            return fields
        elif request.user.role == ROLE_ADMIN:
            return [field for field in fields if field not in ['organization',]]
        return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.role == ROLE_ADMIN:
            org_id = request.user.organization_id
            if db_field.name == "education_level":
                kwargs["queryset"] = EducationLevel.objects.filter(organization_id=org_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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
