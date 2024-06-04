import holidays
from datetime import datetime, date, timedelta

# Populate Availability form choices
def get_choices():
    choices = [
        ('09', '09:00 - 10:00'),
        ('10', '10:00 - 11:00'),
        ('11', '11:00 - 12:00'),
        ('12', '12:00 - 13:00'),
        ('13', '13:00 - 14:00'),
        ('14', '14:00 - 15:00'),
        ('15', '15:00 - 16:00'),
        ('16', '16:00 - 17:00'),
        ('17', '17:00 - 18:00'),
    ]
    return choices

# Show weekday names
def get_weekdays():
    weekday_names = [
        'Segunda-feira',
        'Terça-feira',
        'Quarta-feira',
        'Quinta-feira',
        'Sexta-feira',
        'Sábado',
        'Domingo'
    ]
    return weekday_names

# Show next working days
def get_next_working_days(start_date, num_days):
    br_holidays = holidays.Brazil(years=start_date.year)

    def is_working_day(date):
        return date.weekday() < 6 and date not in br_holidays  # Monday to Saturday and not a public holiday

    working_days = []
    current_date = start_date

    while len(working_days) < num_days:
        if is_working_day(current_date):
            working_days.append(current_date)
        current_date += timedelta(days=1)

    return working_days