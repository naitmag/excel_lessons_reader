import sqlite3 as sq

from models import Lesson


def save_lesson(lesson: Lesson):
    with sq.connect("schedule.db") as con:
        cur = con.cursor()

        cur.execute(
            f"""
            INSERT INTO lesson ('lesson_group', start, end, day, number, lesson_type, name, subgroup, teacher) 
            VALUES ('{lesson.group}',{lesson.start},{lesson.end},{lesson.day},{lesson.number},'{lesson.lesson_type}','{lesson.name}','{lesson.subgroup}','{lesson.teacher}');
            """
        )



