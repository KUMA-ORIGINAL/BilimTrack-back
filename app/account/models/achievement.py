from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill


class Achievement(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название достижения")
    description = models.TextField(verbose_name="Описание достижения")
    photo = ProcessedImageField(upload_to='achievements/%Y/%m',
                                processors=[ResizeToFill(500, 500)],
                                format='JPEG',
                                options={'quality': 60},
                                verbose_name="Фото достижения")
    rarity = models.ForeignKey('Rarity', on_delete=models.PROTECT, related_name='achievements', verbose_name="Редкость")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_achievements', verbose_name="Пользователь")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='user_achievements', verbose_name="Достижение")
    is_opened = models.BooleanField(default=False, verbose_name="Открыто")
    opened_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата открытия")

    class Meta:
        verbose_name = "Пользовательское достижение"
        verbose_name_plural = "Пользовательские достижения"
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user} - {self.achievement} (Открыто: {self.is_opened})"
