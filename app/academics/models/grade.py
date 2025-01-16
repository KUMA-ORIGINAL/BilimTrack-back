from django.contrib.auth import get_user_model
from django.db import models

from academics.models import Subject

User = get_user_model()

class Grade(models.Model):
    GRADE_CHOICES = [
        (0, 'Не был'),
        (10, 'Оценка 10'),
        (20, 'Оценка 20'),
        (30, 'Оценка 30'),
        (40, 'Оценка 40'),
        (50, 'Оценка 50'),
        (60, 'Оценка 60'),
        (70, 'Оценка 70'),
        (80, 'Оценка 80'),
        (90, 'Оценка 90'),
        (100, 'Оценка 100'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.IntegerField(choices=GRADE_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.user.username} - {self.grade}"
