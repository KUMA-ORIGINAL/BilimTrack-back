from django.db import models


class LessonType(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название типа')  # например: Лекция, Практика и т.д.

    class Meta:
        verbose_name = 'Тип занятия'
        verbose_name_plural = 'Типы занятий'

    def __str__(self):
        return self.name
