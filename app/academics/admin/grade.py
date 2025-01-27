from django.contrib import admin

from unfold.admin import ModelAdmin as UnfoldModelAdmin

from academics.models import Grade


@admin.register(Grade)
class GradeAdmin(UnfoldModelAdmin):
    list_display = ('user', 'subject', 'grade', 'comment', 'date')  # отображаемые поля
    list_filter = ('subject', 'grade', 'created_at')  # фильтрация по предметам, оценкам, дате
    search_fields = ('user__username', 'subject__name')  # добавляем поиск по имени пользователя и названию предмета
    ordering = ('-created_at',)  # сортировка по дате создания
    readonly_fields = ('created_at', 'updated_at')  # поля, которые нельзя редактировать

    # Настройка инлайн-редактирования оценок
    fieldsets = (
        (None, {
            'fields': ('user', 'subject', 'grade', 'date', 'comment')
        }),
        ('Таймстемпы', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # сворачиваемая секция
        }),
    )