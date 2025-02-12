from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group

from unfold.admin import ModelAdmin as UnfoldModelAdmin, TabularInline
from unfold.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm

from ..models import User, Skill

admin.site.unregister(Group)


class SkillTabularAdmin(TabularInline):
    model = Skill


@admin.register(User)
class UserAdmin(UserAdmin, UnfoldModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates", {"fields": ("last_login", "date_joined")}),
        ("Общее", {"fields": ('email', 'first_name', 'last_name', 'role', 'photo', )}),
        ('Для студента', {
            'fields': ('achievements', 'group', 'achievements_count',
                        'points', 'rating')}),
        ('Для ментора', {
            'fields': ('tools',)}),
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

    model = User

    ordering = ['date_joined']

    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'group', 'points', 'rating')
    list_display_links = ('id', 'username')
    filter_horizontal = ('achievements', 'tools')
    inlines = [SkillTabularAdmin]
    list_per_page = 20


@admin.register(Group)
class GroupAdmin(GroupAdmin, UnfoldModelAdmin):
    pass