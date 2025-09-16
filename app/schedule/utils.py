import datetime


def get_week_type(date=None):
    if date is None:
        date = datetime.date.today()

    # Определяем номер дня месяца и вычисляем неделю
    week_of_month = (date.day - 1) // 7 + 1

    # нечетные недели -> top, четные -> bottom
    return 'top' if week_of_month % 2 == 1 else 'bottom'