from django.db import models


DAYS_OF_WEEK = [
    (0, 'Понедельник'),
    (1, 'Вторник'),
    (2, 'Среда'),
    (3, 'Четверг'),
    (4, 'Пятница'),
    (5, 'Суббота'),
    (6, 'Воскресенье'),
]

WEEK_TYPES = [
    ('weekly', 'Без деления'),      # Пустое значение — для всех недель
    ('top', 'Числитель'),    # Верхняя неделя
    ('bottom', 'Знаменатель'),  # Нижняя неделя
]


class Schedule(models.Model):
    organization = models.ForeignKey(
        'academics.Organization',
        on_delete=models.CASCADE,
        verbose_name='Учебное заведение'
    )
    education_level = models.ForeignKey(
        'academics.EducationLevel',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Уровень образования',
        related_name='schedules'
    )
    groups = models.ManyToManyField(
        'academics.Group',
        verbose_name='Группы'
    )
    subject = models.ForeignKey(
        'academics.Subject',
        on_delete=models.CASCADE,
        verbose_name='Предмет'
    )
    teacher = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        verbose_name='Преподаватель',
        limit_choices_to={'role': 'mentor'}
    )
    room = models.ForeignKey(
        'Room',
        on_delete=models.CASCADE,
        verbose_name='Аудитория'
    )
    day_of_week = models.IntegerField(
        choices=DAYS_OF_WEEK,
        verbose_name='День недели'
    )
    lesson_time = models.ForeignKey(
        'LessonTime',
        on_delete=models.CASCADE,
        verbose_name='Время пары'
    )
    lesson_type = models.ForeignKey(
        'LessonType',
        on_delete=models.SET_NULL,
        verbose_name='Тип занятия',
        null=True
    )
    week_type = models.CharField(
        max_length=7,
        choices=WEEK_TYPES,
        default='weekly',
        blank=True,
        verbose_name='Тип недели'
    )

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    def __str__(self):
        level = f" [{self.education_level}]" if self.education_level else ""
        group_names = ', '.join([str(g) for g in self.groups.all()])
        return f"{self.organization}{level} - {group_names} - {self.subject} ({self.get_day_of_week_display()}, {self.lesson_time})"
