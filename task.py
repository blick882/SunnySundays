from PyInquirer import prompt
from PyInquirer import Validator, ValidationError

from utils import count_sundays, check_day, format_output


OUTPUT_FILENAME = 'result.log'


class DateValidator(Validator):
    def validate(self, document):
        try:
            day, month, year = map(int, document.text.split('.'))
            assert 1 <= day <= 31
            assert 1 <= month <= 12
            assert 1900 <= year <= 2500

            if year == 2500 and (month != 1 or day != 1):
                raise ValidationError(
                    message='Date ranges from 1 Jan 1900 to 1 Jan 2500',
                    cursor_position=len(document.text)  # Move cursor to the end
                )
        except (ValueError, AssertionError):
            raise ValidationError(
                message='Please enter a valid date in format dd.mm.yyyy',
                cursor_position=len(document.text)  # Move cursor to the end
            )


def date_filter(value):
    day, month, year = map(int, value.split('.'))
    filtered_value = {
        'day': day,
        'month': month,
        'year': year,
        'formatted_date': value,
        'day_of_week': check_day(day, month, year)
    }
    return filtered_value


questions = [
    {
        'type': 'input',
        'name': 'start_date',
        'message': 'Give me the first date:',
        'validate': DateValidator,
        'filter': date_filter,
    },
    {
        'type': 'input',
        'name': 'end_date',
        'message': 'Give me the second date:',
        'validate': DateValidator,
        'filter': date_filter,
    },
    {
        'type': 'list',
        'name': 'output_type',
        'message': 'Would you like to get information on screen, in file or both?',
        'choices': ['screen', 'file', 'both'],
    },
    {
        'type': 'list',
        'name': 'order',
        'message': 'Do you want this information in ascending or descending order?',
        'choices': ['ascending', 'descending'],
    }
]


if __name__ == '__main__':
    answers = prompt(questions)
    total_sundays = count_sundays(answers['start_date'], answers['end_date'])
    result_output = format_output(answers, total_sundays)

    output_type = answers['output_type']
    if output_type in ('screen', 'both'):
        print(result_output)
    if output_type in ('file', 'both'):
        with open(OUTPUT_FILENAME, 'w+') as file:
            file.write(result_output)
