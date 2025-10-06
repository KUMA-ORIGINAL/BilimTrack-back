from django.db.models.signals import pre_save, post_save, post_delete
from django.db.models import F
from django.dispatch import receiver
from .models import Grade


@receiver(pre_save, sender=Grade)
def remember_old_grade(sender, instance, **kwargs):
    """При сохранении оценки запомним старое значение."""
    if instance.pk:
        try:
            instance._old_value = Grade.objects.get(pk=instance.pk).total_score
        except Grade.DoesNotExist:
            instance._old_value = None
    else:
        instance._old_value = None


@receiver(post_save, sender=Grade)
def update_points_on_save(sender, instance, created, **kwargs):
    """После сохранения корректируем баллы студента и группы."""
    user = instance.user

    if created:  # новая оценка
        diff = instance.grade.total_score
    else:  # обновили существующую
        old_value = instance._old_value or 0
        diff = instance.grade.total_score - old_value

    if diff != 0:
        # обновляем счет у студента
        user.__class__.objects.filter(pk=user.pk).update(points=F('points') + diff)

        # обновляем счет у группы, если есть
        if user.group_id:
            user.group.__class__.objects.filter(pk=user.group_id).update(points=F('points') + diff)


@receiver(post_delete, sender=Grade)
def update_points_on_delete(sender, instance, **kwargs):
    """При удалении оценки снимаем её из очков."""
    user = instance.user
    diff = -instance.grade.total_score

    # обновляем счет у студента
    user.__class__.objects.filter(pk=user.pk).update(points=F('points') + diff)

    # обновляем счет у группы, если есть
    if user.group_id:
        user.group.__class__.objects.filter(pk=user.group_id).update(points=F('points') + diff)
