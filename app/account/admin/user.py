from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from ..models import User

@admin.register(User)
class UserAdmin(UserAdmin):
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
        ('required', {
                 'fields': ('email', 'first_name', 'last_name', 'role',
                            'photo', 'achievements', 'group', 'achievements_count',
                            'points', 'rating')}),
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

    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'group', 'is_active')
    list_display_links = ('id', 'username')
    filter_horizontal = ('achievements',)
