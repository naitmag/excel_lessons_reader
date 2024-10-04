from typing import Any

import pandas as pd


def read_excel_data(file_path: str):
    # Путь к файлу

    # Считываем данные из файла
    df = pd.read_excel(file_path, header=None)
    df = df.fillna('')

    # Выводим данные

    def get_groups(data: Any):
        for i in range(len(data)):
            if data[i][0] == '' and data[i][1] == 'время':
                groups = data[i]
                groups = [s.strip() for s in groups]
                groups = [item for item in groups if item not in ['', 'время']]
                return groups, i

    data = df.to_numpy()
    groups, groups_line = get_groups(data)

    schedule = {group: [] for group in groups}

    times = ['8.30\n9.50', '10.05\n11.25', '12.00\n13.20', '13.35\n14.55']
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']

    lesson_day = 0
    lesson_number = 0
    for target_step in data[groups_line + 1:]:
        group_number = 0
        guess_day = target_step[0].replace(' ', '')
        guess_time = target_step[0].replace(' ', '')
        if guess_day in days:
            lesson_day = days.index(guess_day)
        if guess_time in times:
            lesson_number = times.index(guess_time)

        for i in range(2, len(target_step)):

            item = target_step[i]
            if item:
                if item in times or item in days:
                    group_number = 0
                else:
                    print(item)
                    schedule[groups[group_number]].append(f"{lesson_day} {lesson_number} {item}")
                    group_number += 1
            else:
                group_number += 1

    return groups, schedule
