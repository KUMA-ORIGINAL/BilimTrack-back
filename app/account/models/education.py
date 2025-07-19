from django.db import models


class Education(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='educations',
        verbose_name='Пользователь'
    )
    institution = models.CharField(
        max_length=255,
        verbose_name='Учебное заведение'
    )
    field_of_study = models.CharField(
        max_length=255,
        verbose_name='Специальность',
        blank=True,
        null=True
    )
    date = models.CharField(
        max_length=50,
        verbose_name='Дата'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образование'

    def __str__(self):
        return f"{self.field_of_study} в {self.institution}"
