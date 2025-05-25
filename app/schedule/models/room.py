from django.db import models


class Room(models.Model):
    number = models.CharField(
        max_length=10,
        verbose_name='Номер аудитории'
    )
    building = models.CharField(
        max_length=50,
        verbose_name='Здание'
    )

    class Meta:
        verbose_name = 'Аудитория'
        verbose_name_plural = 'Аудитории'

    def __str__(self):
        return f"{self.building} - {self.number}"
