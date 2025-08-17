from django.db import models


class Organization(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название'
    )
    logo = models.FileField(
        upload_to='organizations/logos/',
        verbose_name='Логотип'
    )
    website = models.URLField(
        max_length=255,
        verbose_name='Вебсайт'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Учебное заведение'
        verbose_name_plural = 'Учебные заведения'