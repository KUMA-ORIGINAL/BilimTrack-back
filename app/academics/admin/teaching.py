from django.contrib import admin

from account.models import ROLE_ADMIN
from common.admin import BaseModelAdmin
from ..models import Teaching


@admin.register(Teaching)
class TeachingAdmin(BaseModelAdmin):
    list_display = ('id', 'mentor', 'group', 'subject')
    list_display_links = ('id',)
    list_filter = ('mentor', 'group', 'subject')
    search_fields = (
        'mentor__username',
        'mentor__first_name',
        'mentor__last_name',
        'group__name',
        'subject__name',
    )
    autocomplete_fields = ('mentor', 'group', 'subject')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == ROLE_ADMIN:
            return qs.filter(group__organization_id=request.user.organization_id)
        return qs.none()
