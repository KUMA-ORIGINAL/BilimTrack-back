from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin

from unfold.admin import ModelAdmin as UnfoldModelAdmin, StackedInline
from unfold.contrib.filters.admin import RelatedDropdownFilter
from unfold.contrib.import_export.forms import ImportForm, ExportForm
from unfold.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm

from ..models import User, WorkExperience, Education
from ..resources import UserResource

admin.site.unregister(Group)


class WorkExperienceInline(StackedInline):  # или admin.StackedInline
    model = WorkExperience
    extra = 1  # сколько пустых форм для добавления


class EducationInline(StackedInline):  # или admin.StackedInline
    model = Education
    extra = 1  # сколько пустых форм для добавления


@admin.register(User)
class UserAdmin(UserAdmin, UnfoldModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    resource_classes = [UserResource]

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    model = User

    ordering = ['date_joined']

    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'group', 'points', 'rating')
    list_display_links = ('id', 'username')
    list_filter = ('role',  ("group", RelatedDropdownFilter),
                   'is_active', 'is_staff', 'is_superuser')
    list_filter_submit = True
    autocomplete_fields = ('achievements', 'tools', 'skills')
    inlines = [WorkExperienceInline, EducationInline]
    list_per_page = 20

    fieldsets = (
        (None, {"fields": ("username", "password", 'plain_password')}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    # "user_permissions",
                )
            },
        ),
        ("Dates", {"fields": ("last_login", "date_joined")}),
        ("Общее", {"fields": ('email', 'first_name', 'last_name', 'role', 'photo',)}),
        ('Для студента', {
            'fields': ('group', 'achievements_count',
                       'points', 'rating', 'achievements')}),
        ('Для ментора', {
            'fields': (
                'phone_number',
                'skills',  # Навыки
                'tools',  # Инструменты
                'mentor_achievements',  # Достижения ментора
                'instagram',  # Instagram
                'telegram',  # Telegram
                'whatsapp',  # Whatsapp
                'facebook',  # Facebook
            )
        }),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(Group)
class GroupAdmin(GroupAdmin, UnfoldModelAdmin):
    pass
