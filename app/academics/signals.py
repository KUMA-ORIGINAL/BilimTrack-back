from django.db.models.signals import pre_save, post_save, post_delete
from django.db.models import F
from django.dispatch import receiver
from django.db import transaction
from .models import Grade


class GradeService:
    @staticmethod
    def update_user_points(user_id, diff):
        from account.models import User
        if diff:
            User.objects.filter(pk=user_id).update(points=F("points") + diff)

    @staticmethod
    def update_group_points(group_id, diff):
        from academics.models import Group
        if group_id and diff:
            Group.objects.filter(pk=group_id).update(points=F("points") + diff)

    @classmethod
    def handle_grade_change(cls, grade, old_score=0, is_delete=False):
        diff = -grade.total_score if is_delete else grade.total_score - old_score
        if diff:
            with transaction.atomic():
                cls.update_user_points(grade.user_id, diff)
                group_id = getattr(grade.user, "group_id", None)
                if group_id:
                    cls.update_group_points(group_id, diff)


@receiver(pre_save, sender=Grade)
def remember_old_grade(sender, instance, **kwargs):
    """Сохраняем старое значение, чтобы потом посчитать разницу."""
    if instance.pk:
        old = Grade.objects.filter(pk=instance.pk).only("grade", "attendance").first()
        instance._old_total_score = old.total_score if old else 0
    else:
        instance._old_total_score = 0


@receiver(post_save, sender=Grade)
def update_points_on_save(sender, instance, created, raw=False, **kwargs):
    """Пересчитывает баллы пользователя/группы после изменения оценки."""
    if raw:  # skip loaddata
        return
    old_score = 0 if created else getattr(instance, "_old_total_score", 0)
    GradeService.handle_grade_change(instance, old_score)


@receiver(post_delete, sender=Grade)
def update_points_on_delete(sender, instance, **kwargs):
    """Корректирует баллы при удалении записи."""
    GradeService.handle_grade_change(instance, is_delete=True)