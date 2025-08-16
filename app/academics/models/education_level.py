from django.db import models


class EducationLevel(models.Model):
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
        related_name='education_levels',
        verbose_name='Учебное заведение'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Уровень образования'
    )

    def __str__(self):
        return f"{self.name} ({self.organization})"

    class Meta:
        verbose_name = 'Уровень образования'
        verbose_name_plural = 'Уровни образования'
        unique_together = ('organization', 'name')
