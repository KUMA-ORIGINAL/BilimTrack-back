from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill


class Subject(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    photo = ProcessedImageField(upload_to='subjects/%Y',
                                processors=[ResizeToFill(500, 500)],
                                format='JPEG',
                                options={'quality': 60},
                                blank=True,
                                verbose_name='Фото')
    makalabox_url = models.URLField(blank=True, verbose_name='Ссылка на Makalabox')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name='Учебное заведение')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name']
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
