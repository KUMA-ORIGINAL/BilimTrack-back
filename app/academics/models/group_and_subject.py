from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rules = models.JSONField(blank=True, null=True, help_text="Правила для группы")
    contract = ProcessedImageField(upload_to='contracts/%Y',
                                   processors=[ResizeToFill(500, 500)],
                                   format='JPEG',
                                   options={'quality': 60},
                                   blank=True)
    points = models.PositiveIntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-points']

    def update_group_points(self):
        total_points = self.users.aggregate(total=models.Sum('points'))['total'] or 0
        self.points = total_points
        self.save()


class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = ProcessedImageField(upload_to='subjects/%Y',
                                processors=[ResizeToFill(500, 500)],
                                format='JPEG',
                                options={'quality': 60},
                                blank=True)
    makalabox_url = models.URLField(blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='subjects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.group.name})"

    class Meta:
        unique_together = ('name', 'group')
        ordering = ['name']
