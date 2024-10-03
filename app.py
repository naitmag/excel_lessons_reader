from models import LessonRecord
from reader import read_excel_data
import sqlite3

from sqlite import save_lesson

if __name__ == '__main__':
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
