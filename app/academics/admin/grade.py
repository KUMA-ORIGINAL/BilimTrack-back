from django.contrib import admin

from academics.models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'grade', 'comment', 'created_at', 'updated_at')  # отображаемые поля
    list_filter = ('subject', 'grade', 'created_at')  # фильтрация по предметам, оценкам, дате
    search_fields = ('user__username', 'subject__name')  # добавляем поиск по имени пользователя и названию предмета
    ordering = ('-created_at',)  # сортировка по дате создания
    readonly_fields = ('created_at', 'updated_at')  # поля, которые нельзя редактировать

    # Настройка инлайн-редактирования оценок
    fieldsets = (
        (None, {
            'fields': ('user', 'subject', 'grade', 'comment')
        }),
        ('Таймстемпы', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # сворачиваемая секция
        }),
    )