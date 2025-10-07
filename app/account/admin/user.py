import io
import zipfile

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin

from unfold.admin import ModelAdmin as UnfoldModelAdmin, StackedInline
from unfold.contrib.import_export.forms import ImportForm, ExportForm
from unfold.decorators import action
from unfold.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm

from academics.admin.filters import GroupDropdownFilter
from common.admin import BaseModelAdmin
from ..models import User, WorkExperience, Education, ROLE_ADMIN
from ..resources import StudentResource, MentorResource


admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(GroupAdmin, UnfoldModelAdmin):
    pass


class WorkExperienceInline(StackedInline):  # или admin.StackedInline
    model = WorkExperience
    extra = 0  # сколько пустых форм для добавления


class EducationInline(StackedInline):  # или admin.StackedInline
    model = Education
    extra = 0  # сколько пустых форм для добавления


@admin.register(User)
class UserAdmin(UserAdmin, BaseModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    resource_classes = [StudentResource, MentorResource]

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    model = User

    ordering = ['date_joined']

    list_display_links = ('id', 'username')
    list_filter_submit = True
    autocomplete_fields = ('achievements', 'tools', 'skills', 'groups', 'group')
    inlines = [WorkExperienceInline, EducationInline]
    list_per_page = 20
    readonly_fields = ('date_joined', 'last_login')
    list_select_related = ('organization', 'group')

    actions_list = ["changelist_action"]

    @action(
        description="Экспортировать студентов по группам (XLSX)",
        url_path="changelist-action",
        permissions=["changelist_action"],
    )
    def changelist_action(self, request):
        # Фильтруем только студентов
        students = self.model.objects.filter(role='student').select_related('group')
        student_resource = StudentResource()

        buffer = io.BytesIO()
        zip_file = zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED)

        # Получаем группы студентов
        groups = students.values_list('group__name', flat=True).distinct()

        for group_name in groups:
            users_in_group = students.filter(group__name=group_name)
            dataset = student_resource.export(users_in_group)
            xlsx_data = dataset.xlsx
            file_name = f"{group_name or 'no_group'}.xlsx"
            zip_file.writestr(file_name, xlsx_data)

        zip_file.close()
        buffer.seek(0)

        response = HttpResponse(buffer, content_type="application/zip")
        response["Content-Disposition"] = 'attachment; filename="students_by_groups.zip"'
        return response

    def get_list_filter(self, request):
        list_filter = (
            'role',
            ("group", GroupDropdownFilter),
            'is_active', 'is_staff',
        )
        if request.user.is_superuser:
            return list_filter + ('is_superuser', 'organization',)
        elif request.user.role == ROLE_ADMIN:
            return list_filter
        return list_filter

    def get_readonly_fields(self, request, obj=None, **kwargs):
        readonly_fields = ('points', 'rating', 'achievements_count')
        if request.user.is_superuser:
            return ()
        elif request.user.role == ROLE_ADMIN:
            return readonly_fields
        return readonly_fields

    def get_list_display(self, request, obj=None, **kwargs):
        list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'group', 'points', 'rating', 'organization', 'detail_link')
        if request.user.is_superuser:
            return list_display
        elif request.user.role == ROLE_ADMIN:
            return ('username', 'email', 'first_name', 'last_name', 'role', 'group', 'points', 'rating', 'detail_link')
        return list_display

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == ROLE_ADMIN:
            return qs.filter(organization=request.user.organization)
        return qs.none()

    def get_fieldsets(self, request, obj=None):
        add_fieldsets = (
            (
                None,
                {
                    "classes": ("wide",),
                    "fields": (
                        "username",
                        "password1",
                        "password2",
                        'organization',
                        'role',
                    ),
                },
            ),
        )

        if not obj:
            if request.user.is_superuser:
                return add_fieldsets
            elif request.user.role == ROLE_ADMIN:
                add_fieldsets = (
                    (
                        None,
                        {
                            "classes": ("wide",),
                            "fields": (
                                "username",
                                "password1",
                                "password2",
                                'role',
                            ),
                        },
                    ),
                )
                return add_fieldsets

        fieldsets = [
            (None, {"fields": ("username", "password", "plain_password")}),
            (
                "Permissions",
                {
                    "fields": (
                        "is_staff",
                        "is_active",
                        "is_superuser",
                        "groups",
                    )
                },
            ),
            ("Dates", {"fields": ("last_login", "date_joined")}),
            (
                "Общее",
                {
                    "fields": (
                        "email",
                        "first_name",
                        "last_name",
                        "patronymic",
                        "role",
                        "photo",
                        "organization",
                    )
                },
            ),
            ("Для студента", {"fields": ("group", "achievements_count", "points", "rating",)}),
            (
                "Для ментора",
                {
                    "fields": (
                        "phone_number",
                        'google_meet_link',
                        "skills",
                        "tools",
                        "mentor_achievements",
                        "instagram",
                        "telegram",
                        "whatsapp",
                        "facebook",
                    )
                },
            ),
        ]
        if request.user.is_superuser:
            return fieldsets
        elif request.user.role == ROLE_ADMIN:
            fieldsets = [fs for fs in fieldsets if fs[0] != "Permissions"]
            new_fieldsets = []
            for name, opts in fieldsets:
                if name == "Общее":
                    opts = opts.copy()
                    opts["fields"] = tuple(f for f in opts["fields"] if f != "organization")
                new_fieldsets.append((name, opts))
            fieldsets = new_fieldsets
        return fieldsets

    def save_model(self, request, obj, form, change):
        if request.user.role == ROLE_ADMIN and not change:
            obj.organization_id = request.user.organization_id
        super().save_model(request, obj, form, change)
