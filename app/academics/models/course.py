from django.db import models


class Course(models.Model):
    number = models.PositiveIntegerField(verbose_name='Номер курса')
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Учебное заведение'
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        unique_together = ('number', 'organization')
        ordering = ['organization', 'number']

    def __str__(self):
        org = f"{self.organization}" if self.organization else "Общее"
        return f"{self.number} курс ({org})"
