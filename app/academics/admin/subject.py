from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from unfold.decorators import display

from account.models import ROLE_ADMIN
from common.admin import BaseModelAdmin
from ..models import Subject, EducationLevel, Semester


@admin.register(Subject)
class SubjectAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'description', 'organization', 'display_photo', 'detail_link')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 50

    @display(description=_("Фото"))
    def display_photo(self, obj):
        if obj.photo:
            return mark_safe(
                f'<img src="{obj.photo.url}" height="120" width="120" '
                f'style="border-radius: 10%;" />')

    def get_list_filter(self, request):
        list_filter = ('organization', 'education_level')
        if request.user.role == ROLE_ADMIN:
            list_filter = ('education_level',)
        return list_filter

    def get_list_display(self, request):
        list_display = ('id', 'name', 'description', 'organization', 'education_level', 'display_photo', 'detail_link')
        if request.user.role == ROLE_ADMIN:
            list_display = ('name', 'description', 'education_level', 'display_photo', 'detail_link')
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
            if db_field.name == "semester":
                kwargs["queryset"] = Semester.objects.filter(course__organization_id=org_id)
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
