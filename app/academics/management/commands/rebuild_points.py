from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from academics.models import Group, Grade

User = get_user_model()


class Command(BaseCommand):
    help = "Пересчитать points студентов и групп заново из таблицы Grade (по total_score)"

    def handle(self, *args, **options):
        self.stdout.write("Пересчитываем баллы студентов...")

        for user in User.objects.filter(role='student'):
            grades = Grade.objects.filter(user=user)
            total = sum(g.total_score for g in grades)

            if getattr(user, "points", 0) != total:
                user.points = total
                user.save(update_fields=["points"])

        self.stdout.write("Пересчитываем баллы групп...")

        for group in Group.objects.all():
            total = sum(u.points for u in group.users.all())
            if getattr(group, "points", 0) != total:
                group.points = total
                group.save(update_fields=["points"])

        self.stdout.write(self.style.SUCCESS("Готово ✅"))
