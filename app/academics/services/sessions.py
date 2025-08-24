import datetime

from schedule.models import Schedule
from ..models import Session


def generate_sessions_for_date(target_date: datetime.date) -> int:
    """
    Создаёт занятия (Session) на заданную дату по расписанию (Schedule).
    Возвращает количество созданных сессий.
    """
    weekday = target_date.weekday()
    week_number = target_date.isocalendar()[1]
    is_top_week = (week_number % 2 == 1)

    created_count = 0
    schedules = Schedule.objects.filter(day_of_week=weekday)

    for schedule in schedules:
        # проверяем тип недели
        if schedule.week_type == "top" and not is_top_week:
            continue
        if schedule.week_type == "bottom" and is_top_week:
            continue

        lesson_time = schedule.lesson_time

        session, created = Session.objects.get_or_create(
            subject=schedule.subject,
            teacher=schedule.teacher,
            room=schedule.room,
            date=target_date,
            start_time=lesson_time.start_time,
            end_time=lesson_time.end_time,
            defaults={"is_active": True}
        )

        # прикрепляем группы (даже если уже создано раньше)
        session.groups.add(*schedule.groups.all())

        if created:
            created_count += 1

    return created_count
