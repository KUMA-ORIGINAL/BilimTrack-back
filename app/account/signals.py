from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from .models import User

@receiver(m2m_changed, sender=User.achievements.through)
def update_achievements_count(sender, instance, **kwargs):
    instance.achievements_count = instance.achievements.count()
    instance.save()

def update_group_points(group):
    total_points = group.users.aggregate(total=models.Sum('points'))['total'] or 0
    group.points = total_points
    group.save()

@receiver(post_save, sender=User)
def update_group_points_on_user_save(sender, instance, **kwargs):
    if instance.group:
        update_group_points(instance.group)
