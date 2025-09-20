from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Sum
from academics.models import Group

User = get_user_model()


class Command(BaseCommand):
    help = "Пересчитать points студентов и групп заново из таблицы Grade"

    def handle(self, *args, **options):
        self.stdout.write("Пересчитываем баллы студентов...")

        for user in User.objects.all():
            total = user.grade_set.aggregate(total=Sum('grade'))['total'] or 0
            if user.points != total:
                user.points = total
                user.save(update_fields=['points'])

        self.stdout.write("Пересчитываем баллы групп...")

        for group in Group.objects.all():
            total = group.users.aggregate(total=Sum('points'))['total'] or 0
            if group.points != total:
                group.points = total
                group.save(update_fields=['points'])

        self.stdout.write(self.style.SUCCESS("Готово ✅"))
