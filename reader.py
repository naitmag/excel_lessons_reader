from typing import Any

import pandas as pd
from enum import Enum


# def parse_schedule(entry):
#     result = {'day': entry[0], 'number': entry[1], 'weeks': [], 'types': [], 'raw': entry}
#     i = 2
#     while ',' in entry[i]:
#         result['weeks'].append(entry[i].replace(',', ''))
#         i += 1
#     result['weeks'].append(entry[i])
#
#     lessons_types = ['лаб.', 'пр.', 'л.', 'сем.']
#     i += 1
#     while ',' in entry[i]:
#         result['types'].append(entry[i])
#         i += 1
#
#     if entry[i] in lessons_types:
#         result['types'].append(entry[i])
#
#     return result

def parse_lesson(entry):
    class ArgTypes(Enum):
        WEEKS = 0
        LESSON_TYPE = 1
        NAME = 2
        TEACHER = 3
        SUBGROUP = 4

    result = {
        'day': entry[0],
        'number': entry[1],
        'weeks': [],
        'types': [],
        'name': [],
        'subgroup': [],
        'teacher': [],
        'raw': entry
    }

    def detect_type(arg: str):

        if arg.replace(',', '').replace('-', '').isdigit():
            return ArgTypes.WEEKS.value
        lessons_types = ['лаб.', 'пр.', 'л.', 'сем.']
        if arg.replace(',', '') in lessons_types:
            return ArgTypes.LESSON_TYPE.value
        if len(arg) == 4 and arg.upper() == arg:
            return ArgTypes.TEACHER.value
        if '(' in arg or ')' in arg:
            return ArgTypes.SUBGROUP.value
        if arg.upper() == arg:
            return ArgTypes.NAME.value

    search_types = True
    for arg in entry[2:]:
        arg_type = detect_type(arg)

        if arg_type == ArgTypes.WEEKS.value:
            result['weeks'].append(arg)
        elif search_types and arg_type == ArgTypes.LESSON_TYPE.value:
            result['types'].append(arg)
        elif arg_type == ArgTypes.NAME.value:
            search_types = False
            result['name'].append(arg)
        elif arg_type == ArgTypes.SUBGROUP.value:
            result['subgroup'].append(arg)
        else:
            result['teacher'].append(arg)
    if not result['weeks']:
        result['weeks'].append('1-17')
    if not result['types']:
        result['types'].append('-')
    return result


class Lesson:
    def __init__(self, data: dict):
        self.day = data['day']
        self.number = data['number']
        self.weeks = self.parse_weeks(data['weeks'], data['types'])
        self.types = data['types']
        self.name = ' '.join(data['name'])
        self.teacher = ' '.join(data['teacher'])
        self.raw = data['raw']
        self.test = []

    @staticmethod
    def parse_weeks(weeks, types):
        n = len(weeks)
        m = len(types)
        result = []
        if n == m:
            result = [(weeks[i], types[i]) for i in range(n)]
        elif n > m:
            if m == 1:
                return [(week, types[0]) for week in weeks]
            else:
                i = 0
                for week in weeks:
                    if ',' in week and ',' in types[i]:
                        i += 1
                    result.append((week, types[i]))
        elif n < m:
            if n == 1:
                result.append((weeks[0], '/'.join(types)))
            else:
                for i in range(n):
                    if i == n - 1:
                        result.append((weeks[i], '/'.join(types[n - 1:])))
                        return result
                    result.append((weeks[i], types[i]))
        return result


# Путь к файлу
file_path = "data1.xlsx"

# Считываем данные из файла
df = pd.read_excel(file_path, header=None)
df = df.fillna('')


# Выводим данные

def get_groups(data: Any):
    for i in range(len(data)):
        if data[i][0] == '' and data[i][1] == 'время':
            return i


data = df.to_numpy()
groups_line = get_groups(data)

groups = data[groups_line]
groups = [s.strip() for s in groups]
groups = [item for item in groups if item not in ['', 'время']]

schedule = {group: [] for group in groups}

target_step = data[14]

times = ['8.30\n9.50', '10.05\n11.25', '12.00\n13.20', '13.35\n14.55']
days = ['п о н е д е л ь н и к', 'в т о р н и к', 'с р е д а', 'ч е т в е р г', 'п я т н и ц а', 'с у б б о т а']

lesson_day = 0
lesson_number = 0
for target_step in data[groups_line + 1:]:
    group_number = 0
    if target_step[0] in days:
        lesson_day = days.index(target_step[0])
    if target_step[1] in times:
        lesson_number = times.index(target_step[1])
    for i in range(2, len(target_step)):

        item = target_step[i]
        if item:
            if item in times or item in days:
                group_number = 0
            else:
                schedule[groups[group_number]].append(f"{lesson_day} {lesson_number} {item}")
                group_number += 1
        else:
            group_number += 1

print('Input target group:')
print(groups)
target = '308'
result = schedule[target]

for item in result:
    data = item.split()
    res = parse_lesson(data)

    lesson = Lesson(res)
    print(' '.join(lesson.raw[2:]))
    print(lesson.weeks)
