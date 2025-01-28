from django.contrib.auth import get_user_model
from django.db import models

from academics.models import Subject

User = get_user_model()

class Grade(models.Model):
    GRADE_CHOICES = [
        (0, 'Не был'),
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет')
    grade = models.IntegerField(choices=GRADE_CHOICES, verbose_name='Оценка')
    date = models.DateField(verbose_name='Дата')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return f"{self.user.username} - {self.grade}"
