from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class GroupSubjectMentor(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name='Группа')
    mentor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Наставник',
        limit_choices_to={'role': 'mentor'}
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        unique_together = ('group', 'mentor')
        verbose_name = 'Связка: группа–наставник'
        verbose_name_plural = 'Связки: группа–наставник'

    def __str__(self):
        return f'{self.group} | {self.mentor}'


class GroupSubjectMentorSubject(models.Model):
    group_subject_mentor = models.ForeignKey(GroupSubjectMentor, on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name='Предмет')

    class Meta:
        unique_together = ('group_subject_mentor', 'subject')
        verbose_name = 'Предмет связки'
        verbose_name_plural = 'Предметы связки'

    def __str__(self):
        return f'{self.group_subject_mentor.group} | {self.subject} | {self.group_subject_mentor.mentor}'
