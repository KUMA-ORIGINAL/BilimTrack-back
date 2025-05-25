from django.db import models


class LessonTime(models.Model):
    start_time = models.TimeField(
        verbose_name='Время начала'
    )
    end_time = models.TimeField(
        verbose_name='Время окончания'
    )

    class Meta:
        verbose_name = 'Время пары'
        verbose_name_plural = 'Время пар'

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


