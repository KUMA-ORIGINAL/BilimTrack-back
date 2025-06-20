from django.db import models


class WorkExperience(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='work_experiences', verbose_name='Пользователь')
    position = models.CharField(max_length=255, verbose_name='Место работы')  # Frontend
    company = models.CharField(max_length=255, verbose_name='Компания')        # Codify Academy
    start_date = models.CharField(max_length=50, verbose_name='Дата начала')   # 03.04
    end_date = models.CharField(max_length=50, verbose_name='Дата окончания')  # Настоящее время
    description = models.TextField(verbose_name='Описание', blank=True, null=True)  # Интегрировал api

    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыт работы'

    def __str__(self):
        return f"{self.position} в {self.company}"
