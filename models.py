from enum import Enum


class Lesson:
    def __init__(self, day: str, number: str, interval: str = None, lesson_type: str = None, name: str = None,
                 teacher: str = None,
                 subgroup: list = None, group: str = None):
        self.day = int(day)
        self.number = int(number)
        self.start, self.end = self.parse_interval(interval)
        self.lesson_type = lesson_type
        self.name = name
        self.teacher = teacher
        self.subgroup = ' '.join(subgroup)
        self.group = group

    @staticmethod
    def parse_interval(interval: str) -> tuple:
        if not '-' in interval:
            return (int(interval),) * 2

        return tuple(map(int, interval.split('-')))

    def __str__(self):
        return f"{self.group} | {self.day}| {self.number} | {self.start} | {self.end} | {self.lesson_type} | {self.name} | {self.subgroup} | {self.teacher}"


class LessonRecord:
    def __init__(self, data: list, group: str):
        data = self.parse_lesson(data)
        self.day = data['day']
        self.number = data['number']
        self.weeks = self.parse_weeks(data['weeks'], data['types'])
        self.name = ' '.join(data['name'])
        self.teacher = ' '.join(data['teacher'])
        self.subgroup = data['subgroup']
        self.group = group
        self.raw = data['raw']

    def __str__(self):
        return f"{self.weeks} {self.name} {self.teacher}"

    def get_list(self) -> list:
        result = []
        for item in self.weeks:
            lesson = Lesson(
                day=self.day,
                number=self.number,
                interval=item[0],
                lesson_type=item[1],
                name=self.name,
                teacher=self.teacher,
                subgroup=self.subgroup,
                group=self.group
            )
            result.append(lesson)

        return result

    @staticmethod
    def clean_records(data: list | tuple):
        return [item.replace(',', '') for item in data]

    @staticmethod
    def parse_lesson(entry):
        default_max_week = 17

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
            if '.' in arg and arg.replace(',', '') in lessons_types:
                return ArgTypes.LESSON_TYPE.value
            if len(arg) == 4 and arg.upper() == arg:
                return ArgTypes.TEACHER.value
            if '(' in arg or ')' in arg:
                return ArgTypes.SUBGROUP.value
            if arg.upper() == arg:
                return ArgTypes.NAME.value

        search_types = True
        for arg in entry[2:]:
            skip_chars = ['-', '/']
            if not arg in skip_chars:

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
            result['weeks'].append(f'1-{default_max_week}')
        if not result['types']:
            result['types'].append('-')
        return result

    def parse_weeks(self, weeks, types):
        n = len(weeks)
        m = len(types)
        result = []

        if not (n > m != 1):
            weeks = self.clean_records(weeks)
            types = self.clean_records(types)

        if n == m:
            result = [(weeks[i], types[i]) for i in range(n)]
        elif n > m:
            if m == 1:
                return [(week, types[0]) for week in weeks]
            else:
                i = 0
                for week in self.clean_records(weeks):
                    if ',' in week and ',' in types[i]:
                        i += 1
                    result.append((week, types[i].replace(',', '')))
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
