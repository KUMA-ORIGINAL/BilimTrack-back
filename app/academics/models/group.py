from django.contrib.auth import get_user_model
from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill

User = get_user_model()

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название группы')
    rules = models.JSONField(blank=True, null=True, help_text="Правила для группы", verbose_name='Правила')
    contract = ProcessedImageField(upload_to='contracts/%Y',
                                   processors=[ResizeToFill(500, 500)],
                                   format='JPEG',
                                   options={'quality': 60},
                                   blank=True,
                                   verbose_name='Контракт')
    points = models.PositiveIntegerField(default=0, blank=True, verbose_name='Очки')
    subjects = models.ManyToManyField('Subject', related_name='groups', verbose_name='Предметы')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='groups', verbose_name='Курс', blank=True, null=True)
    curator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mentored_groups',
        verbose_name='Куратор',
        limit_choices_to={'role': 'mentor'}
    )
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE,
                                     verbose_name='Учебное заведение')
    education_level = models.ForeignKey(
        'academics.EducationLevel',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Уровень образования',
        related_name='groups'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-points']
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def update_group_points(self):
        total_points = 0
        for user in self.users.all():
            user_points = user.grade_set.aggregate(total=models.Sum('grade'))['total'] or 0
            total_points += user_points
        self.points = total_points
        self.save()
