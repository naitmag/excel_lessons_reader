from models import LessonRecord, Week
from reader import read_excel_data

from sqlite import save_lesson


def save_lessons():
    groups, schedule = read_excel_data('data1.xlsx')
    print('Input target group:')
    print(groups)

    for group in groups:
        result = schedule[group]
        for item in result:
            data = item.split()
            record = LessonRecord(data, group)
            result = record.get_list()
            for less in result:
                save_lesson(less)


if __name__ == '__main__':
    week = Week('308', 5)
    print(week.format_week())