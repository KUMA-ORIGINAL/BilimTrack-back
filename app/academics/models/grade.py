from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Grade(models.Model):
    GRADE_CHOICES = [
        (0, 'Оценки нету'),
        (1, 'Оценка 1'),
        (2, 'Оценка 2'),
        (3, 'Оценка 3'),
        (4, 'Оценка 4'),
        (5, 'Оценка 5'),
        (6, 'Оценка 6'),
        (7, 'Оценка 7'),
        (8, 'Оценка 8'),
        (9, 'Оценка 9'),
        (10, 'Оценка 10'),
    ]
    ATTENDANCE_CHOICES = [
        ('A', 'Присутствовал'),
        ('B', 'Отработка'),
        ('C', 'Опоздал'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Студент', limit_choices_to={'role': 'student'})
    session = models.ForeignKey('Session', on_delete=models.CASCADE, verbose_name='Занятие')
    grade = models.IntegerField(
        choices=GRADE_CHOICES,
        verbose_name='Оценка',
        blank=True, null=True
    )
    attendance = models.CharField(
        choices=ATTENDANCE_CHOICES,
        max_length=1,
        verbose_name='Посещение',
        blank=True, null=True
    )
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    make_up_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на отработку')
    make_up_file = models.FileField(upload_to='makeup_submissions/%Y/%m', blank=True, null=True, verbose_name='Файл отработки')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        unique_together = ('user', 'session')  # Один студент — одна оценка за пару
        ordering = ('-created_at',)
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return f"{self.user.username} - {self.grade} ({self.session})"

    @property
    def total_score(self):
        """
        Итоговый балл по системе:
            10 × вес × (оценка / 5)
        Если оценки нет или 0 → базовый балл за посещение:
            A=5, B=4, C=4, N=0
        """
        weights = {
            'A': 1.0,
            'B': 0.9,
            'C': 0.8,
            'N': 0.0,
        }
        base_points = {
            'A': 5,
            'B': 4,
            'C': 4,
            'N': 0,
        }

        weight = weights.get(self.attendance, 0.0)
        grade = self.grade or 0

        if grade > 0:
            result = 10 * weight * (grade / 5)
        else:
            result = base_points.get(self.attendance, 0)

        return round(result)
