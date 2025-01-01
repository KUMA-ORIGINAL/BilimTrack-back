from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill


class Rarity(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Achievement(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = ProcessedImageField(upload_to='achievements/%Y/%m',
                                processors=[ResizeToFill(500, 500)],
                                format='JPEG',
                                options={'quality': 60})
    rarity = models.ForeignKey(Rarity, on_delete=models.PROTECT, related_name='achievements')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
