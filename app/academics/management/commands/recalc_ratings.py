from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = "Пересчитать рейтинг студентов на основе points"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Пересчитываем рейтинг студентов...")

        students = list(User.objects.filter(role="student").order_by("-points", "id"))

        for idx, student in enumerate(students, start=1):
            student.rating = idx

        User.objects.bulk_update(students, ["rating"])

        self.stdout.write(self.style.SUCCESS("✅ Рейтинг студентов обновлён"))
