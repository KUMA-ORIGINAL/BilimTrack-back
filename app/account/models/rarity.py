from django.db import models

class Rarity(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название редкости")

    class Meta:
        verbose_name = "Редкость"
        verbose_name_plural = "Редкости"

    def __str__(self):
        return self.name
