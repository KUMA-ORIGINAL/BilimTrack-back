from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class LessonTopic(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name='Предмет')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ментор')
    title = models.CharField(max_length=255, verbose_name="Тема")

    class Meta:
        verbose_name = "Тема урока"
        verbose_name_plural = "Темы уроков"
        unique_together = ('subject', 'mentor', 'title')

    def __str__(self):
        return self.title
