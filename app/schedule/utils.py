import datetime

SEMESTER_START = datetime.date(2025, 9, 1)  # начало учебного периода


def get_week_type(date=None):
    if date is None:
        date = datetime.date.today()

    # сколько недель прошло с начала учебного года
    delta_weeks = (date - SEMESTER_START).days // 7

    return 'top' if delta_weeks % 2 == 0 else 'bottom'
