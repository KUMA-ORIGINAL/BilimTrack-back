from django.db import models


class Semester(models.Model):
    number = models.PositiveSmallIntegerField(
        verbose_name='Номер семестра'
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='semesters',
        verbose_name='Курс'
    )
    start_date = models.DateField(null=True, blank=True, verbose_name='Дата начала')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата окончания')

    class Meta:
        verbose_name = 'Семестр'
        verbose_name_plural = 'Семестры'
        unique_together = ('number', 'course')  # например: "1 семестр 1 курса"
        ordering = ['course', 'number']

    def __str__(self):
        return f"{self.number} семестр ({self.course})"
