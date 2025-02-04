from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Grade


@receiver(post_save, sender=Grade)
def update_points(sender, instance, **kwargs):
    user = instance.user

    user_points = user.grade_set.aggregate(total=models.Sum('grade'))['total'] or 0
    user.points = user_points
    user.save()

    group = user.group
    if group:
        group.update_group_points()
