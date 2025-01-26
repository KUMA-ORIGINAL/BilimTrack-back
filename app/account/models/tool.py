from django.db import models


class Tool(models.Model):
    name = models.CharField(verbose_name='Инструмент', max_length=255)
    logo = models.FileField(verbose_name='Лого инструмента', upload_to='programs/program-tools/')
    description = models.CharField(verbose_name='Описание инструмента', max_length=255)

    class Meta:
        verbose_name = "Технология"
        verbose_name_plural = "Технологии"

    def __str__(self):
        return self.name
