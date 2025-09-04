from django.db import models


class Course(models.Model):
    number = models.PositiveIntegerField(verbose_name='Номер курса')
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
        verbose_name='Учебное заведение'
    )
    education_level = models.ForeignKey(
        'academics.EducationLevel',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Уровень образования',
        related_name='courses'
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        unique_together = ('number', 'organization', 'education_level')
        ordering = ['organization', 'number']

    def __str__(self):
        edu_level = f"{self.education_level}" if self.education_level else "Общее"
        return f"{self.number} курс ({edu_level})"
