from models import LessonRecord
from reader import read_excel_data

if __name__ == '__main__':
    groups, schedule = read_excel_data('data1.xlsx')
    print('Input target group:')
    print(groups)
    target = input()
    result = schedule[target]

    for item in result:
        data = item.split()
        record = LessonRecord(data)
        result = record.get_list()
        print("Record:")
        print(' '.join(record.raw))
        input()
        print("Added to db:")
        for less in result:
            print(less)
            input()
