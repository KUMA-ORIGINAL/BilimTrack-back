from django.db import models


class Skill(models.Model):
    name = models.CharField(verbose_name='Навык', max_length=255)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='skills')

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name
