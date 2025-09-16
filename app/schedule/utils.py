import datetime


def get_week_type(date=None):
    if date is None:
        date = datetime.date.today()
    week_number = date.isocalendar()[1]  # номер недели
    return 'top' if week_number % 2 else 'bottom'
