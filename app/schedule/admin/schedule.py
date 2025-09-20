from django.contrib import admin
from unfold.contrib.filters.admin import RelatedDropdownFilter, ChoicesDropdownFilter

from academics.admin.filters import MentorDropdownFilter, GroupDropdownFilter, EducationLevelFilter, \
    LessonTimeDropdownFilter, CourseDropdownFilter
from academics.models import Group, EducationLevel
from account.models import ROLE_ADMIN
from common.admin import BaseModelAdmin
from ..models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(BaseModelAdmin):
    list_display_links = ('id', 'get_groups', 'subject')
    list_filter_submit = True
    search_fields = (
        'subject__name',
        'teacher__full_name',
        'room__number',
    )
    autocomplete_fields = ('groups', 'subject', 'teacher', 'room', 'lesson_time')

    def get_list_filter(self, request):
        list_filter = (
            ('day_of_week', ChoicesDropdownFilter),
            ('lesson_type', ChoicesDropdownFilter),
            ('lesson_time', RelatedDropdownFilter),
            ('groups', GroupDropdownFilter),
            ('teacher', MentorDropdownFilter),
            ('groups__course', RelatedDropdownFilter),
            'education_level',
            'organization'
        )
        if request.user.role == ROLE_ADMIN:
            list_filter = (
                ('day_of_week', ChoicesDropdownFilter),
                ('lesson_type', ChoicesDropdownFilter),
                ('lesson_time', LessonTimeDropdownFilter),
                ('groups', GroupDropdownFilter),
                ('teacher', MentorDropdownFilter),
                ('groups__course', CourseDropdownFilter),
                EducationLevelFilter,
            )
        return list_filter

    @admin.display(description='Группы')
    def get_groups(self, obj):
        return ", ".join([str(g) for g in obj.groups.all()])

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.role == ROLE_ADMIN:
            org_id = request.user.organization_id
            if db_field.name == "education_level":
                kwargs["queryset"] = EducationLevel.objects.filter(organization_id=org_id)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if request.user.role == ROLE_ADMIN and db_field.name == "groups":
            kwargs["queryset"] = Group.objects.filter(organization_id=request.user.organization_id)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_list_display(self, request):
        base = (
            'id', 'get_groups', 'subject', 'teacher',
            'day_of_week', 'week_type', 'lesson_time', 'lesson_type', 'room',
            'education_level',
        )
        if request.user.is_superuser:
            base = base + ('organization',)
        return base + ('detail_link',)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if request.user.is_superuser:
            return fields
        elif request.user.role == ROLE_ADMIN:
            return [f for f in fields if f != 'organization']
        return fields

    def save_model(self, request, obj, form, change):
        if request.user.role == ROLE_ADMIN and not change:
            obj.organization_id = request.user.organization_id
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request).prefetch_related('groups')
        if request.user.is_superuser:
            return qs
        elif request.user.role == ROLE_ADMIN:
            return qs.filter(organization_id=request.user.organization_id)
        return qs.none()
