from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import User

@receiver(m2m_changed, sender=User.achievements.through)
def update_achievements_count(sender, instance, **kwargs):
    instance.achievements_count = instance.achievements.count()
    instance.save()

