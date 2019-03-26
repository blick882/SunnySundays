from datetime import datetime


MONTHS_DICT = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}


def check_day(day, month, year):
    days = [1, 2, 3, 4, 5, 6, 7]
    a = (14 - month) // 12
    y = year - a
    m = month + 12 * a - 2
    result = ((
        (day + y + y // 4 - y // 100 + y // 400 + (31 * m) // 12)) % 7) - 1
    return days[result]


def count_sundays(start_date, end_date):
    total_sundays = 0
    result = []

    start = datetime.strptime(start_date['formatted_date'], '%d.%m.%Y')
    end = datetime.strptime(end_date['formatted_date'], '%d.%m.%Y')

    if end < start:
        start_date, end_date = end_date, start_date

    while start_date['day'] < end_date['day'] or start_date['month'] < end_date[
            'month'] or start_date['year'] < end_date['year']:
        if start_date['day_of_week'] == 7:
            total_sundays += 1
            start_date['day_of_week'] = 1
            result.append("{}.{}.{}".format(start_date['day'], start_date['month'], start_date['year']))
        else:
            start_date['day_of_week'] += 1

        if start_date['day'] == MONTHS_DICT[start_date['month']]:
            # leap logic
            if start_date['month'] == 2 and start_date['year'] % 4 == 0:
                if str(start_date['year'])[-2:] != "00" or (
                        str(start_date['year'])[-2:] == "00"
                        and start_date['year'] % 400 == 0):
                    start_date['day'] += 1
                else:
                    start_date['day'] = 1
                    start_date['month'] += 1
            # ending year
            elif start_date['month'] == 12:
                start_date['day'] = 1
                start_date['month'] = 1
                start_date['year'] += 1

            else:
                start_date['day'] = 1
                start_date['month'] += 1
        # Leap year
        elif start_date['day'] > MONTHS_DICT[start_date['month']]:
            start_date['day'] = 1
            start_date['month'] += 1

        else:
            start_date['day'] += 1

    return result


def format_output(answers, days_list):
    result_output = "Counting Sundays\nStarting date: {}\n".format(answers['start_date']['formatted_date'])
    order = 1 if answers['order'] == 'ascending' else -1

    for day in days_list[::order]:
        result_output += "{}\n".format(day)
    result_output += "Ending date: {}\n\n".format(answers['end_date']['formatted_date'])
    return result_output
