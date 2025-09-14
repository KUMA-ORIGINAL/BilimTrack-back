from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Teaching(models.Model):
    mentor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'mentor'},
        verbose_name='Наставник'
    )
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name='Группа')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name='Предмет')

    class Meta:
        unique_together = ('mentor', 'group', 'subject')
        verbose_name = 'Преподавание'
        verbose_name_plural = 'Преподавания'

    def __str__(self):
        return f"{self.mentor} → {self.subject} ({self.group})"
