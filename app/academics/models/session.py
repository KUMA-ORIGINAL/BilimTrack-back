import uuid
from django.db import models


class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    subject = models.ForeignKey(
        'academics.Subject',
        on_delete=models.CASCADE,
        verbose_name='Предмет'
    )
    topic = models.ForeignKey(
        'LessonTopic',
        on_delete=models.SET_NULL,
        verbose_name="Тема урока",
        blank=True,
        null=True
    )

    groups = models.ManyToManyField(
        'academics.Group',
        verbose_name="Группы"
    )
    teacher = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        verbose_name="Преподаватель",
        limit_choices_to={'role': 'mentor'}
    )
    room = models.ForeignKey(
        'schedule.Room',
        on_delete=models.CASCADE,
        verbose_name="Аудитория"
    )

    date = models.DateField(verbose_name='Дата занятия')
    start_time = models.TimeField(verbose_name='Начало занятия')
    end_time = models.TimeField(verbose_name='Конец занятия')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        unique_together = (
            'subject',
            'teacher',
            'room',
            'date',
            'start_time',
            'end_time'
        )

    def __str__(self):
        groups = ", ".join([str(g) for g in self.groups.all()[:3]])
        if self.groups.count() > 3:
            groups += "..."
        return f"{self.subject} [{groups}] | {self.date} {self.start_time}-{self.end_time}"