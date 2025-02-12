from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from account.models import User
from .models import Grade


@receiver(post_save, sender=Grade)
def update_points_on_save(sender, instance, **kwargs):
    update_user_and_group_points(instance)


@receiver(post_delete, sender=Grade)
def update_points_on_delete(sender, instance, **kwargs):
    update_user_and_group_points(instance)


def update_user_and_group_points(grade_instance):
    user = grade_instance.user

    user_points = user.grade_set.aggregate(total=models.Sum('grade'))['total'] or 0
    user.points = user_points
    user.save()

    # Обновляем рейтинг пользователя
    update_users_rating()

    group = user.group
    if group:
        group.update_group_points()

def update_users_rating():
    all_users = User.objects.order_by('-points')

    for rank, user in enumerate(all_users, 1):
        user.rating = rank
        user.save()
