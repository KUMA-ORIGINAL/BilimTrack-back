from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class GroupSubjectMentor(models.Model):
    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        verbose_name='Группа'
    )
    subject = models.ForeignKey(
        'Subject',
        on_delete=models.CASCADE,
        verbose_name='Предмет'
    )
    mentor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Наставник',
        limit_choices_to={'role': 'mentor'}
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено'
    )

    class Meta:
        unique_together = ('group', 'subject', 'mentor')
        verbose_name = 'Связка: группа-предмет-наставник'
        verbose_name_plural = 'Связки: группа-предмет-наставник'

    def __str__(self):
        return f'{self.group} | {self.subject} | {self.mentor}'
