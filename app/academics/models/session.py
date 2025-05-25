import uuid
from django.db import models


class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name='Предмет')
    date = models.DateField(verbose_name='Дата занятия')
    start_time = models.TimeField(verbose_name='Начало занятия')
    end_time = models.TimeField(verbose_name='Конец занятия')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self):
        return f"{self.subject.name} | {self.date} {self.start_time}-{self.end_time}"
