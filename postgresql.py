import psycopg2
from openpyxl import Workbook
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Postgresql:
    def __init__(self, connection):
        self.connection = connection
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self._cur = self.connection.cursor()

    def get_user(self, id_user):
        try:
            self._cur.execute(f"SELECT * FROM users WHERE id_user = {id_user} LIMIT 1")
            res = self._cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

        return False

    def get_user_by_login(self, login):
        try:
            self._cur.execute(f"SELECT * FROM users WHERE login = '{login}' LIMIT 1")
            res = self._cur.fetchone()

            if not res:
                print("Пользователь не найден")
                return False

            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))
        return False

    def update_user_avatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = psycopg2.Binary(avatar)
            self._cur.execute(f"UPDATE users SET avatar = {binary} WHERE id_user = {user_id}")
        except psycopg2.Error as e:
            print("Ошибка обновления аватара в БД: " + str(e))
            return False
        return True

    def get_count_students(self):
        try:
            self._cur.execute(f"SELECT COUNT(*) AS count_row FROM students")
            res, = self._cur.fetchone()
            if res:
                return res
            return 0
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_count_oo(self):
        try:
            self._cur.execute(f"SELECT COUNT(*) AS count_row FROM oo WHERE year = '2021'")
            res, = self._cur.fetchone()
            if res:
                return res
            return 0
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_count_of_subject(self):
        try:
            self._cur.execute(f"SELECT COUNT(*) AS count_row FROM subjects")
            res, = self._cur.fetchone()
            if res:
                return res
            return 0
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_count_of_parallels(self):
        try:
            self._cur.execute(f"SELECT COUNT(*) AS count_row FROM parallels")
            res, = self._cur.fetchone()
            if res:
                return res
            return 0
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_all_parallels(self, year):
        try:
            self._cur.execute(f"""
            SELECT parallel FROM parallels 
                WHERE parallel in 
                (
                    SELECT DISTINCT parallel FROM oo_parallels 
                        WHERE id_oo in 
                        (
                            SELECT id_oo FROM oo WHERE year = '{year}'
                        )
                );""")
            res = self._cur.fetchall()
            if res:
                return res
            return []

        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_parallels_for_oo(self, id_oo):
        try:
            self._cur.execute(f"SELECT id_oo_parallels, parallel FROM oo_parallels WHERE id_oo = {id_oo}")
            res = self._cur.fetchall()
            if res:
                return res
        except psycopg2.Error as e:
            print("Ошибка получения статей из БД " + str(e))
        return []

    def get_subject_id(self, subject_name):
        try:
            self._cur.execute(
                f"SELECT id_subjects FROM subjects WHERE subject_name = '{subject_name.replace(' ', '_')}'")
            res, = self._cur.fetchone()
            if res:
                return res
        except psycopg2.Error as e:
            print("Ошибка получения статей из БД " + str(e))
            return []

    def get_subject_name(self, id_subjects):

        try:
            if id_subjects:
                self._cur.execute(f"SELECT subject_name FROM subjects"
                                  f" WHERE id_subjects = {id_subjects}")
                res = self._cur.fetchone()
                if res:
                    return res[0].replace("_", " ")
                return ""
        except psycopg2.Error as e:
            print("Ошибка получения статей из БД " + str(e))


    def get_subjects_for_oo_parallels(self, id_oo_parallels):
        try:
            if id_oo_parallels:
                self._cur.execute(f"SELECT id_oo_parallels_subjects, id_subjects FROM oo_parallels_subjects"
                                  f" WHERE id_oo_parallels = {id_oo_parallels}")
                res = self._cur.fetchall()
                if res:
                    return [[x[0], self.get_subject_name(x[1])] for x in res]

        except psycopg2.Error as e:
            print("Ошибка получения статей из БД " + str(e))
        return []

    def get_id_oo_parallels(self, parallel, id_oo):
        try:
            self._cur.execute(
                f"SELECT id_oo_parallels FROM oo_parallels WHERE parallel = {parallel} AND id_oo = {id_oo}")
            res, = self._cur.fetchone()
            if not res:
                print("id_oo_parallels не был найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_oo_parallels_subjects(self, id_subjects, id_oo_parallels):
        try:
            self._cur.execute(
                f" SELECT id_oo_parallels_subjects FROM oo_parallels_subjects "
                f" WHERE id_oo_parallels = {id_oo_parallels}"
                f" AND id_subjects = {id_subjects}")
            res, = self._cur.fetchone()
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_district_for_report_type_2(self, parallel, id_subjects, year):
        try:
            self._cur.execute(f"""
            SELECT id_district, district_name FROM district 
            WHERE id_district IN 
            (
                SELECT DISTINCT id_district FROM name_of_the_settlement 
                WHERE id_name_of_the_settlement IN 
                (
                    SELECT DISTINCT id_name_of_the_settlement FROM oo 
                    WHERE year = '{year}' 
                    AND id_oo in 
                    (
                        SELECT id_oo FROM oo_parallels 
                        WHERE parallel = {parallel} 
                        AND id_oo_parallels in 
                        (
                            SELECT id_oo_parallels FROM oo_parallels_subjects 
                            WHERE id_subjects = {id_subjects}
                        )
                    )
                )
            );""")

            res = self._cur.fetchall()
            if res:
                return res
            return []
        except psycopg2.Error as e:
            print("Ошибка получения муниципалитетов из БД " + str(e))

    def get_districts(self, id_user, year):
        try:
            self._cur.execute(
                f"""
                SELECT id_district, district_name FROM district 
                WHERE id_district IN 
                (
                    SELECT DISTINCT id_district FROM name_of_the_settlement 
                    WHERE id_name_of_the_settlement IN 
                    (
                        SELECT DISTINCT id_name_of_the_settlement FROM oo 
                        WHERE year = '{year}'
                        AND oo_login in 
                        (
                            SELECT oo_login FROM users_oo_logins 
                            WHERE id_user = {id_user}
                        )
                    )
                );""")
            res = self._cur.fetchall()
            if res:
                return res
        except psycopg2.Error as e:
            print("Ошибка получения муниципалитетов из БД " + str(e))
        return []

    def get_subjects(self, parallel, id_user, id_district, year):
        try:
            if id_district != "all":
                self._cur.execute(f"""
                SELECT id_subjects, subject_name FROM subjects 
                WHERE id_subjects in 
                (
                    SELECT id_subjects FROM oo_parallels_subjects 
                    WHERE id_oo_parallels in 
                        (
                            SELECT id_oo_parallels FROM oo_parallels 
                            WHERE id_oo in 
                                (
                                    SELECT id_oo FROM oo 
                                    WHERE id_name_of_the_settlement in 
                                        (
                                            SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                                            WHERE id_district = {id_district}
                                        )
                                )
                                AND parallel = {parallel} 
                                AND id_oo in 
                                (
                                    (
                                    SELECT id_oo FROM oo 
                                    WHERE year='{year}' 
                                    AND oo_login in 
                                            (
                                                SELECT oo_login FROM users_oo_logins 
                                                WHERE id_user = {id_user}
                                            )
                                    )
                                )
                        )
                );""")
            else:
                self._cur.execute(f"""
                SELECT id_subjects, subject_name FROM subjects 
                    WHERE id_subjects IN 
                        (
                            SELECT DISTINCT id_subjects FROM oo_parallels_subjects 
                            WHERE id_oo_parallels IN 
                            (
                                SELECT id_oo_parallels FROM oo_parallels 
                                WHERE parallel={parallel} 
                                AND id_oo in 
                                    (
                                        SELECT id_oo FROM oo 
                                        WHERE year='{year}' 
                                        AND oo_login in 
                                            (
                                                SELECT oo_login FROM users_oo_logins 
                                                WHERE id_user = {id_user}
                                            )
                                    )
                            )
                        )
                    ;""")
            res = self._cur.fetchall()
            if res:
                return [[x[0], x[1].replace("_", " ")] for x in res]
            return []
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_comparison_of_ratings_for_all_districts(self, id_subjects, parallel, year):
        try:
            self._cur.execute(f"""SELECT result, COUNT(result) FROM
                                    (SELECT id_students,
                                    CASE WHEN mark_for_vpr<mark_for_last_semester THEN 'понизил'
                                        WHEN mark_for_vpr>mark_for_last_semester THEN 'повысил'
                                        WHEN mark_for_vpr=mark_for_last_semester THEN 'подтвердил'
                                    END AS result
                                    FROM (SELECT id_students,sum_marks, mark_for_last_semester,
                                            CASE WHEN sum_marks<mark_three THEN 2
                                                WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                                                WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                                                WHEN sum_marks>=mark_five THEN 5
                                                ELSE 0
                                            END AS mark_for_vpr FROM 
                                (SELECT id_students, sum_marks, mark_for_last_semester, mark_three, mark_four, mark_five FROM 
                                    ((SELECT id_students, mark_for_last_semester, id_oo_parallels_subjects, SUM(mark) as sum_marks FROM result_for_task 
                                        WHERE id_oo_parallels_subjects IN 
                                            (SELECT id_oo_parallels_subjects FROM oo_parallels_subjects 
                                                WHERE id_oo_parallels IN 
                                                    (SELECT id_oo_parallels FROM oo_parallels 
                                                        WHERE parallel={parallel} AND id_oo in 
                                                            (SELECT id_oo FROM oo 
                                                                WHERE year='{year}'))
                                                AND id_subjects={id_subjects}) GROUP BY id_students, id_oo_parallels_subjects, mark_for_last_semester) AS t1

                                        LEFT JOIN (SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five FROM oo_parallels_subjects 
                                                WHERE id_oo_parallels IN 
                                                    (SELECT id_oo_parallels FROM oo_parallels 
                                                        WHERE parallel={parallel})
                                                AND id_subjects={id_subjects}) AS t2 
                                        USING (id_oo_parallels_subjects))) AS t3) AS t4) AS t5 GROUP BY result;""")
            res = self._cur.fetchall()
            if res:
                count_of_all_students = 0
                increased = 0
                confirmed = 0
                downgraded = 0

                for row in res:
                    if row[0] == "повысил":
                        increased = row[1]
                    elif row[0] == "подтвердил":
                        confirmed = row[1]
                    elif row[0] == "понизил":
                        downgraded = row[1]
                    count_of_all_students += int(row[1])

                return {"Понизили": {"count_of_students": downgraded,
                                     "%": round((downgraded / count_of_all_students) * 100, 2)},
                        "Подтвердили": {"count_of_students": confirmed,
                                        "%": round((confirmed / count_of_all_students) * 100, 2)},
                        "Повысили": {"count_of_students": increased,
                                     "%": round((increased / count_of_all_students) * 100,
                                                2)},
                        "Всего": {"count_of_students": count_of_all_students,
                                  "%": 100}}

            return {},
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_comparison_of_ratings_for_all_schools_in_district(self, id_district, id_subjects, parallel, year):
        try:
            self._cur.execute(f"""
            SELECT result, COUNT(result) FROM
            (SELECT id_students,
            CASE WHEN mark_for_vpr<mark_for_last_semester THEN 'понизил'
                WHEN mark_for_vpr>mark_for_last_semester THEN 'повысил'
                WHEN mark_for_vpr=mark_for_last_semester THEN 'подтвердил'
            END AS result
            FROM (SELECT id_students,sum_marks, mark_for_last_semester,
                    CASE WHEN sum_marks<mark_three THEN 2
                        WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                        WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                        WHEN sum_marks>=mark_five THEN 5
                        ELSE 0
                    END AS mark_for_vpr FROM 
        (SELECT id_students, sum_marks, mark_for_last_semester, mark_three, mark_four, mark_five FROM 
            ((SELECT id_students, mark_for_last_semester, id_oo_parallels_subjects, SUM(mark) as sum_marks FROM result_for_task 
                WHERE id_oo_parallels_subjects IN 
                    (SELECT id_oo_parallels_subjects FROM oo_parallels_subjects 
                        WHERE id_oo_parallels IN 
                            (SELECT id_oo_parallels FROM oo_parallels 
                                WHERE parallel={parallel} AND id_oo in 
                                    (SELECT id_oo FROM oo 
                                        WHERE year='{year}'
                                            AND id_name_of_the_settlement in 
                                                (SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                                                    WHERE id_district = {id_district})))
                        AND id_subjects={id_subjects}) GROUP BY id_students, id_oo_parallels_subjects, mark_for_last_semester) AS t1

                LEFT JOIN (SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five FROM oo_parallels_subjects 
                        WHERE id_oo_parallels IN 
                            (SELECT id_oo_parallels FROM oo_parallels 
                                WHERE parallel={parallel} AND id_oo in 
                                    (SELECT id_oo FROM oo 
                                        WHERE year='{year}'
                                            AND id_name_of_the_settlement in 
                                                (SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                                                    WHERE id_district = {id_district})))
                        AND id_subjects={id_subjects}) AS t2 
                USING (id_oo_parallels_subjects))) AS t3) AS t4) AS t5 GROUP BY result;""")
            res = self._cur.fetchall()
            if res:
                count_of_all_students = 0
                increased = 0
                confirmed = 0
                downgraded = 0

                for row in res:
                    if row[0] == "повысил":
                        increased = row[1]
                    elif row[0] == "подтвердил":
                        confirmed = row[1]
                    elif row[0] == "понизил":
                        downgraded = row[1]
                    count_of_all_students += int(row[1])

                return {"Понизили": {"count_of_students": downgraded,
                                     "%": round((downgraded / count_of_all_students) * 100, 2)},
                        "Подтвердили": {"count_of_students": confirmed,
                                        "%": round((confirmed / count_of_all_students) * 100, 2)},
                        "Повысили": {"count_of_students": increased,
                                     "%": round((increased / count_of_all_students) * 100,
                                                2)},
                        "Всего": {"count_of_students": count_of_all_students,
                                  "%": 100}}

            return {},
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_count_students_mark_for_all_districts(self, id_subjects, parallel, year):
        try:
            self._cur.execute(f"""SELECT value, COUNT(value) FROM
                                    (SELECT id_students,sum_marks,
                                            CASE WHEN sum_marks<mark_three THEN 2
                                                WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                                                WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                                                WHEN sum_marks>=mark_five THEN 5
                                                ELSE 0
                                            END AS value FROM 
                                (SELECT id_students, sum_marks, mark_three, mark_four, mark_five FROM 
                                    ((SELECT id_students, id_oo_parallels_subjects, SUM(mark) as sum_marks FROM result_for_task 
                                        WHERE id_oo_parallels_subjects IN 
                                            (SELECT id_oo_parallels_subjects FROM oo_parallels_subjects 
                                                WHERE id_oo_parallels IN 
                                                    (SELECT id_oo_parallels FROM oo_parallels 
                                                        WHERE parallel={parallel} AND id_oo in 
                                                            (SELECT id_oo FROM oo 
                                                                WHERE year='{year}'))
                                                AND id_subjects={id_subjects}) GROUP BY id_students, id_oo_parallels_subjects) AS t1

                                        LEFT JOIN (SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five FROM oo_parallels_subjects 
                                                WHERE id_oo_parallels IN 
                                                    (SELECT id_oo_parallels FROM oo_parallels 
                                                        WHERE parallel={parallel} AND id_oo in 
                                                            (SELECT id_oo FROM oo 
                                                                WHERE year='{year}'))
                                                AND id_subjects={id_subjects}) AS t2 
                                        USING (id_oo_parallels_subjects))) AS t3) AS t4 GROUP BY value ORDER BY (value);""")
            res = self._cur.fetchall()
            if res:

                mark_dict = {x[0]: x[1] for x in res}
                count_of_all_mark = sum(mark_dict.values())
                if mark_dict.get(2) is None:
                    count_of_mark_two = 0
                else:
                    count_of_mark_two = mark_dict[2]

                if mark_dict.get(3) is None:
                    count_of_mark_three = 0
                else:
                    count_of_mark_three = mark_dict[3]

                if mark_dict.get(4) is None:
                    count_of_mark_four = 0
                else:
                    count_of_mark_four = mark_dict[4]

                if mark_dict.get(5) is None:
                    count_of_mark_five = 0
                else:
                    count_of_mark_five = mark_dict[5]
                return {2: round((count_of_mark_two / count_of_all_mark) * 100, 2),
                        3: round((count_of_mark_three / count_of_all_mark) * 100, 2),
                        4: round((count_of_mark_four / count_of_all_mark) * 100, 2),
                        5: round((count_of_mark_five / count_of_all_mark) * 100, 2)}, count_of_all_mark
            return {},

        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_parallels(self, id_user, id_district, year):
        try:
            self._cur.execute(f"""SELECT DISTINCT parallel FROM oo_parallels WHERE id_oo in 
                                    (SELECT id_oo FROM oo 
                                        WHERE oo_login in 
                                        (SELECT oo_login FROM users_oo_logins 
                                            WHERE id_user = {id_user})
                                        AND id_name_of_the_settlement IN 
                                            (SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                                                WHERE id_district = {id_district})
                                        AND year = '{year}'
                                    );""")
            res = self._cur.fetchall()
            if res:
                return res
            return []
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_oo_from_district(self, id_district, id_user, year):
        try:
            self._cur.execute(f"""
            SELECT id_oo, oo_name FROM oo 
                WHERE id_oo NOT IN 
                (SELECT id_oo FROM oo_levels_of_the_educational_program 
                    WHERE id_levels_of_the_educational_program = 4 AND value = 'Да') 
                AND id_name_of_the_settlement IN 
                (SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                    WHERE id_district = {id_district}) 
                AND id_oo IN 
                (SELECT id_oo FROM oo_parallels)
                AND oo_login in 
                (SELECT oo_login FROM users_oo_logins 
                    WHERE id_user = {id_user})
                AND year = '{year}';""")
            res = self._cur.fetchall()
            if res:
                return res
            return []

        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_oo_from_id_oo_parallels_subjects(self, id_district, id_user, parallel, id_subjects):
        try:
            self._cur.execute(f"""
            SELECT id_oo_parallels_subjects, id_oo_parallels FROM oo_parallels_subjects 
                WHERE id_oo_parallels in 
                    (SELECT id_oo_parallels FROM oo_parallels 
                        WHERE id_oo in (SELECT id_oo FROM oo 
                            WHERE id_oo NOT IN 
                            (SELECT id_oo FROM oo_levels_of_the_educational_program 
                                WHERE id_levels_of_the_educational_program = 4 AND value = 'Да') 
                        AND id_name_of_the_settlement IN 
                            (SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                                WHERE id_district = {id_district}) 
                        AND parallel = {parallel}
                        AND oo_login in 
                            (SELECT oo_login FROM users_oo_logins 
                                WHERE id_user = {id_user}))) 
                AND id_subjects = {id_subjects};""")
            res = self._cur.fetchall()
            if res:
                return res
            return []

        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_oo_name_from_oo_parallels(self, id_oo_parallels):
        try:
            self._cur.execute(f"""SELECT oo_name FROM oo WHERE id_oo in 
                                    (SELECT id_oo FROM oo_parallels WHERE id_oo_parallels = {id_oo_parallels})""")
            res, = self._cur.fetchone()
            if res:
                return res
            return ""
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_comparison_of_ratings(self, id_oo_parallels_subjects, id_oo_parallels):
        try:
            self._cur.execute(f"""
            SELECT result, COUNT(result) FROM
                (SELECT id_students,
                CASE WHEN mark_for_vpr<mark_for_last_semester THEN 'понизил'
                    WHEN mark_for_vpr>mark_for_last_semester THEN 'повысил'
                    WHEN mark_for_vpr=mark_for_last_semester THEN 'подтвердил'
                END AS result
                FROM (SELECT id_students,sum_marks, mark_for_last_semester,
                    CASE WHEN sum_marks<mark_three THEN 2
                    WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                    WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                    WHEN sum_marks>=mark_five THEN 5
                    ELSE 0
                    END AS mark_for_vpr
                FROM (SELECT id_students, sum_marks, mark_three, mark_four, mark_five, mark_for_last_semester  
                FROM (SELECT id_students, id_oo_parallels_subjects, mark_for_last_semester, SUM(mark) as sum_marks 
                    FROM result_for_task 
                    WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects} AND id_oo_parallels = {id_oo_parallels}
                    GROUP BY id_students, id_oo_parallels_subjects, mark_for_last_semester) AS t1
                LEFT JOIN 
                    (SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five 
                    FROM oo_parallels_subjects 
                    WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects}) AS t2
                    USING (id_oo_parallels_subjects)) AS t3) AS t4) AS t5 GROUP BY result;""")
            res = self._cur.fetchall()
            if res:
                count_of_all_students = 0
                increased = 0
                confirmed = 0
                downgraded = 0

                for row in res:
                    if row[0] == "повысил":
                        increased = row[1]
                    elif row[0] == "подтвердил":
                        confirmed = row[1]
                    elif row[0] == "понизил":
                        downgraded = row[1]
                    count_of_all_students += int(row[1])

                return {"Понизили": {"count_of_students": downgraded,
                                     "%": round((downgraded / count_of_all_students) * 100, 2)},
                        "Подтвердили": {"count_of_students": confirmed,
                                        "%": round((confirmed / count_of_all_students) * 100, 2)},
                        "Повысили": {"count_of_students": increased,
                                     "%": round((increased / count_of_all_students) * 100,
                                                2)},
                        "Всего": {"count_of_students": count_of_all_students, "%": 100}}

            return {}
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_count_students_mark_for_all_school_in_district(self, id_district, id_subjects, parallel, year):
        try:
            self._cur.execute(f"""SELECT value, COUNT(value) FROM
                                                (SELECT id_students,sum_marks,
                                                        CASE WHEN sum_marks<mark_three THEN 2
                                                            WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                                                            WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                                                            WHEN sum_marks>=mark_five THEN 5
                                                            ELSE 0
                                                        END AS value FROM 
                                            (SELECT id_students, sum_marks, mark_three, mark_four, mark_five FROM 
                                                ((SELECT id_students, id_oo_parallels_subjects, SUM(mark) as sum_marks FROM result_for_task 
                                                    WHERE id_oo_parallels_subjects IN 
                                                        (SELECT id_oo_parallels_subjects FROM oo_parallels_subjects 
                                                            WHERE id_oo_parallels IN 
                                                                (SELECT id_oo_parallels FROM oo_parallels 
                                                                    WHERE parallel={parallel} AND id_oo in 
                                                                        (SELECT id_oo FROM oo 
                                                                            WHERE year='{year}'
                                                                                AND id_name_of_the_settlement in 
                                                                                    (SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                                                                                        WHERE id_district = {id_district})))
                                                            AND id_subjects={id_subjects}) GROUP BY id_students, id_oo_parallels_subjects) AS t1

                                                    LEFT JOIN (SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five FROM oo_parallels_subjects 
                                                            WHERE id_oo_parallels IN 
                                                                (SELECT id_oo_parallels FROM oo_parallels 
                                                                    WHERE parallel={parallel} AND id_oo in 
                                                                        (SELECT id_oo FROM oo 
                                                                            WHERE year='{year}'
                                                                                AND id_name_of_the_settlement in 
                                                                                    (SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                                                                                        WHERE id_district = {id_district})))
                                                            AND id_subjects={id_subjects}) AS t2 
                                                    USING (id_oo_parallels_subjects))) AS t3) AS t4 GROUP BY value ORDER BY (value);""")
            res = self._cur.fetchall()
            if res:
                if res:
                    mark_dict = {x[0]: x[1] for x in res}
                    count_of_all_mark = sum(mark_dict.values())
                    if mark_dict.get(2) is None:
                        count_of_mark_two = 0
                    else:
                        count_of_mark_two = mark_dict[2]

                    if mark_dict.get(3) is None:
                        count_of_mark_three = 0
                    else:
                        count_of_mark_three = mark_dict[3]

                    if mark_dict.get(4) is None:
                        count_of_mark_four = 0
                    else:
                        count_of_mark_four = mark_dict[4]

                    if mark_dict.get(5) is None:
                        count_of_mark_five = 0
                    else:
                        count_of_mark_five = mark_dict[5]
                    return {2: round((count_of_mark_two / count_of_all_mark) * 100, 2),
                            3: round((count_of_mark_three / count_of_all_mark) * 100, 2),
                            4: round((count_of_mark_four / count_of_all_mark) * 100, 2),
                            5: round((count_of_mark_five / count_of_all_mark) * 100, 2)}, count_of_all_mark
                return {},

        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_count_students_mark(self, id_oo_parallels_subjects, id_oo_parallels):
        try:
            self._cur.execute(f"""
                    SELECT value, COUNT(value) FROM
                        (SELECT id_students,sum_marks,
                                CASE WHEN sum_marks<mark_three THEN 2
                                    WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                                WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                                WHEN sum_marks>=mark_five THEN 5
                                    ELSE 0
                                END AS value
                                FROM (SELECT id_students, sum_marks, mark_three, mark_four, mark_five  
                                FROM (SELECT id_students, id_oo_parallels_subjects, SUM(mark) as sum_marks 
                                    FROM result_for_task 
                                    WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects} AND id_oo_parallels = {id_oo_parallels}
                                    GROUP BY id_students, id_oo_parallels_subjects) AS t1
                                LEFT JOIN 
                                    (SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five 
                                    FROM oo_parallels_subjects 
                                    WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects}) AS t2
                                    USING (id_oo_parallels_subjects)) AS t3)
                        AS t4 GROUP BY value;""")
            res = self._cur.fetchall()
            if res:
                mark_dict = {x[0]: x[1] for x in res}
                count_of_all_mark = sum(mark_dict.values())
                if mark_dict.get(2) is None:
                    count_of_mark_two = 0
                else:
                    count_of_mark_two = mark_dict[2]

                if mark_dict.get(3) is None:
                    count_of_mark_three = 0
                else:
                    count_of_mark_three = mark_dict[3]

                if mark_dict.get(4) is None:
                    count_of_mark_four = 0
                else:
                    count_of_mark_four = mark_dict[4]

                if mark_dict.get(5) is None:
                    count_of_mark_five = 0
                else:
                    count_of_mark_five = mark_dict[5]
                return {2: round((count_of_mark_two / count_of_all_mark) * 100, 2),
                        3: round((count_of_mark_three / count_of_all_mark) * 100, 2),
                        4: round((count_of_mark_four / count_of_all_mark) * 100, 2),
                        5: round((count_of_mark_five / count_of_all_mark) * 100, 2)}, count_of_all_mark
            return {},
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_result_vpr(self, id_oo_parallels_subjects, id_oo_parallels):
        try:
            self._cur.execute(f"""
                    SELECT value, COUNT(value) FROM
                        (SELECT id_students,sum_marks,
                                CASE WHEN sum_marks<mark_three THEN 2
                                    WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                                WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                                WHEN sum_marks>=mark_five THEN 5
                                    ELSE 0
                                END AS value
                                FROM (SELECT id_students, sum_marks, mark_three, mark_four, mark_five  
                                FROM (SELECT id_students, id_oo_parallels_subjects, SUM(mark) as sum_marks 
                                    FROM result_for_task 
                                    WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects} AND id_oo_parallels = {id_oo_parallels}
                                    GROUP BY id_students, id_oo_parallels_subjects) AS t1
                                LEFT JOIN 
                                    (SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five 
                                    FROM oo_parallels_subjects 
                                    WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects}) AS t2
                                    USING (id_oo_parallels_subjects)) AS t3)
                        AS t4 GROUP BY value ORDER BY (value);""")
            res = self._cur.fetchall()
            if res:
                mark_dict = {x[0]: x[1] for x in res}
                count_of_all_mark = sum(mark_dict.values())
                if mark_dict.get(2) is None:
                    count_of_mark_two = 0
                else:
                    count_of_mark_two = mark_dict[2]

                if mark_dict.get(3) is None:
                    count_of_mark_three = 0
                else:
                    count_of_mark_three = mark_dict[3]

                if mark_dict.get(4) is None:
                    count_of_mark_four = 0
                else:
                    count_of_mark_four = mark_dict[4]

                if mark_dict.get(5) is None:
                    count_of_mark_five = 0
                else:
                    count_of_mark_five = mark_dict[5]

                mean = round(((
                                      2 * count_of_mark_two + 3 * count_of_mark_three + 4 * count_of_mark_four + 5 * count_of_mark_five) / count_of_all_mark),
                             1)

                two = round((count_of_mark_two / count_of_all_mark) * 100, 1)
                three = round((count_of_mark_three / count_of_all_mark) * 100, 1)
                four = round((count_of_mark_four / count_of_all_mark) * 100, 1)
                five = round((count_of_mark_five / count_of_all_mark) * 100, 1)
                quality = round(four + five, 1)
                if quality > 100:
                    quality = 100
                performance = round(three + four + five, 1)
                if performance > 100:
                    performance = 100

                return {"2": two,
                        "3": three,
                        "4": four,
                        "5": five,
                        "mean_mark": mean,
                        "count_of_students": count_of_all_mark,
                        "quality": quality,
                        "performance": performance}
            return {}

        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_result_vpr_for_all_school_in_district(self, id_district, id_subjects, parallel, year):
        try:
            self._cur.execute(f"""
            SELECT value, COUNT(value) FROM
            (SELECT id_students,sum_marks,
                    CASE WHEN sum_marks<mark_three THEN 2
                        WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                        WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                        WHEN sum_marks>=mark_five THEN 5
                        ELSE 0
                    END AS value FROM 
        (SELECT id_students, sum_marks, mark_three, mark_four, mark_five FROM 
            ((SELECT id_students, id_oo_parallels_subjects, SUM(mark) as sum_marks FROM result_for_task 
                WHERE id_oo_parallels_subjects IN 
                    (SELECT id_oo_parallels_subjects FROM oo_parallels_subjects 
                        WHERE id_oo_parallels IN 
                            (SELECT id_oo_parallels FROM oo_parallels 
                                WHERE parallel={parallel} AND id_oo in 
                                    (SELECT id_oo FROM oo 
                                        WHERE year='{year}'
                                            AND id_name_of_the_settlement in 
                                                (SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                                                    WHERE id_district = {id_district})))

                        AND id_subjects={id_subjects}) GROUP BY id_students, id_oo_parallels_subjects) AS t1

                LEFT JOIN (SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five FROM oo_parallels_subjects 
                        WHERE id_oo_parallels IN 
                            (SELECT id_oo_parallels FROM oo_parallels 
                                WHERE parallel={parallel} AND id_oo in 
                                    (SELECT id_oo FROM oo 
                                        WHERE year='{year}'
                                            AND id_name_of_the_settlement in 
                                                (SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                                                    WHERE id_district = {id_district})))
                        AND id_subjects={id_subjects}) AS t2 
                USING (id_oo_parallels_subjects))) AS t3) AS t4 GROUP BY value ORDER BY (value);""")
            res = self._cur.fetchall()
            if res:
                mark_dict = {x[0]: x[1] for x in res}
                count_of_all_mark = sum(mark_dict.values())
                if mark_dict.get(2) is None:
                    count_of_mark_two = 0
                else:
                    count_of_mark_two = mark_dict[2]

                if mark_dict.get(3) is None:
                    count_of_mark_three = 0
                else:
                    count_of_mark_three = mark_dict[3]

                if mark_dict.get(4) is None:
                    count_of_mark_four = 0
                else:
                    count_of_mark_four = mark_dict[4]

                if mark_dict.get(5) is None:
                    count_of_mark_five = 0
                else:
                    count_of_mark_five = mark_dict[5]
                mean = round(((
                                      2 * count_of_mark_two + 3 * count_of_mark_three + 4 * count_of_mark_four + 5 * count_of_mark_five) / count_of_all_mark),
                             1)

                two = round((count_of_mark_two / count_of_all_mark) * 100, 1)
                three = round((count_of_mark_three / count_of_all_mark) * 100, 1)
                four = round((count_of_mark_four / count_of_all_mark) * 100, 1)
                five = round((count_of_mark_five / count_of_all_mark) * 100, 1)
                quality = round(four + five, 1)
                if quality > 100:
                    quality = 100
                performance = round(three + four + five, 1)
                if performance > 100:
                    performance = 100

                return {"2": two,
                        "3": three,
                        "4": four,
                        "5": five,
                        "mean_mark": mean,
                        "count_of_students": count_of_all_mark,
                        "quality": quality,
                        "performance": performance}
            return {}

        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_result_vpr_for_all_districts(self, id_subjects, parallel, year):
        try:
            self._cur.execute(f"""SELECT value, COUNT(value) FROM
                                    (SELECT id_students,sum_marks,
                                            CASE WHEN sum_marks<mark_three THEN 2
                                                WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                                                WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                                                WHEN sum_marks>=mark_five THEN 5
                                                ELSE 0
                                            END AS value FROM 
                                (SELECT id_students, sum_marks, mark_three, mark_four, mark_five FROM 
                                    ((SELECT id_students, id_oo_parallels_subjects, SUM(mark) as sum_marks FROM result_for_task 
                                        WHERE id_oo_parallels_subjects IN 
                                            (SELECT id_oo_parallels_subjects FROM oo_parallels_subjects 
                                                WHERE id_oo_parallels IN 
                                                    (SELECT id_oo_parallels FROM oo_parallels 
                                                        WHERE parallel={parallel} AND id_oo in 
                                                            (SELECT id_oo FROM oo 
                                                                WHERE year='{year}'))
                                                AND id_subjects={id_subjects}) GROUP BY id_students, id_oo_parallels_subjects) AS t1

                                        LEFT JOIN (SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five FROM oo_parallels_subjects 
                                                WHERE id_oo_parallels IN 
                                                    (SELECT id_oo_parallels FROM oo_parallels 
                                                        WHERE parallel={parallel} AND id_oo in 
                                                            (SELECT id_oo FROM oo 
                                                                WHERE year='{year}'))
                                                AND id_subjects={id_subjects}) AS t2 
                                        USING (id_oo_parallels_subjects))) AS t3) AS t4 GROUP BY value ORDER BY (value);""")
            res = self._cur.fetchall()
            if res:
                mark_dict = {x[0]: x[1] for x in res}
                count_of_all_mark = sum(mark_dict.values())
                if mark_dict.get(2) is None:
                    count_of_mark_two = 0
                else:
                    count_of_mark_two = mark_dict[2]

                if mark_dict.get(3) is None:
                    count_of_mark_three = 0
                else:
                    count_of_mark_three = mark_dict[3]

                if mark_dict.get(4) is None:
                    count_of_mark_four = 0
                else:
                    count_of_mark_four = mark_dict[4]

                if mark_dict.get(5) is None:
                    count_of_mark_five = 0
                else:
                    count_of_mark_five = mark_dict[5]

                mean = round(((
                                      2 * count_of_mark_two + 3 * count_of_mark_three + 4 * count_of_mark_four + 5 * count_of_mark_five) / count_of_all_mark),
                             1)
                two = round((count_of_mark_two / count_of_all_mark) * 100, 1)
                three = round((count_of_mark_three / count_of_all_mark) * 100, 1)
                four = round((count_of_mark_four / count_of_all_mark) * 100, 1)
                five = round((count_of_mark_five / count_of_all_mark) * 100, 1)
                quality = round(four + five, 1)
                if quality > 100:
                    quality = 100
                performance = round(three + four + five, 1)
                if performance > 100:
                    performance = 100

                return {"2": two,
                        "3": three,
                        "4": four,
                        "5": five,
                        "mean_mark": mean,
                        "count_of_students": count_of_all_mark,
                        "quality": quality,
                        "performance": performance}
            return {}

        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_districts_for_schools_in_risk(self, id_user, year):
        try:
            self._cur.execute(f"""
            SELECT id_district, district_name FROM district 
            WHERE id_district in 
                (
                    SELECT id_district FROM name_of_the_settlement 
                    WHERE id_name_of_the_settlement in 
                    (
                        SELECT id_name_of_the_settlement FROM oo 
                        WHERE id_oo in 
                        (
                            SELECT id_oo FROM schools_in_risk 
                            WHERE year = '{year}'
                        )
                        AND oo_login in 
                        (
                            SELECT oo_login FROM users_oo_logins 
                            WHERE id_user = {id_user}
                        )
                    )
                );""")
            res = self._cur.fetchall()
            if res:
                return res
            return 0
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_oo_by_district_for_schools_in_risk(self, year, id_district, id_user):

        try:
            self._cur.execute(f"""
            SELECT id_oo, oo_name FROM oo 
            WHERE id_name_of_the_settlement in 
            (
                SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                WHERE id_district = {id_district}
            )
            AND id_oo in 
            (
                SELECT id_oo FROM schools_in_risk 
                WHERE year = '{year}'
            )
            AND oo_login in 
            (
                SELECT oo_login FROM users_oo_logins 
                WHERE id_user = {id_user}
            );""")
            res = self._cur.fetchall()
            if res:
                return res
            return []
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_parallels_for_schools_in_risk(self, year, id_district, id_oo):
        try:
            if id_district == "all":
                self._cur.execute(f"""
                SELECT DISTINCT parallel FROM schools_in_risk 
                WHERE year = '{year}'
                order by (parallel);""")

            elif id_oo == "all":
                self._cur.execute(f"""
                SELECT DISTINCT parallel FROM schools_in_risk 
                WHERE year = '{year}' 
                AND id_oo in 
                (
                    SELECT id_oo FROM oo 
                    WHERE id_name_of_the_settlement in 
                    (
                        SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                        WHERE id_district = {id_district}
                    )
                )
                order by (parallel) ;""")

            else:
                self._cur.execute(f"""
                SELECT DISTINCT parallel FROM schools_in_risk 
                WHERE year = '{year}' 
                AND id_oo = {id_oo}
                order by (parallel) ;""")

            res = self._cur.fetchall()
            if res:
                return res
            return []
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_subject_for_school_in_risk(self, year, id_district, id_oo, parallel):
        try:
            if id_district == "all":
                self._cur.execute(f"""
                SELECT DISTINCT id_subjects FROM schools_in_risk 
                WHERE year = '{year}' 
                AND parallel = {parallel}
                ;""")

            elif id_oo == "all":
                self._cur.execute(f"""
                SELECT DISTINCT id_subjects FROM schools_in_risk 
                WHERE year = '{year}' 
                AND parallel = {parallel}
                AND id_oo in 
                (
                    SELECT id_oo FROM oo 
                    WHERE id_name_of_the_settlement in 
                    (
                        SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                        WHERE id_district = {id_district}
                    )
                )
                ;""")

            else:
                self._cur.execute(f"""
                SELECT DISTINCT id_subjects FROM schools_in_risk 
                WHERE year = '{year}' 
                AND parallel = {parallel}
                AND id_oo = {id_oo}
                ;""")
            res = self._cur.fetchall()
            if res:
                return [(x[0], self.get_subject_name(id_subjects=x[0])) for x in res]
            return []
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_school_login(self, id_oo):
        try:
            self._cur.execute(f"""SELECT oo_login FROM oo WHERE id_oo = {id_oo};""")
            res, = self._cur.fetchone()
            if res:
                return res
            return []
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_district_name(self, id_district):
        try:
            self._cur.execute(f"""SELECT district_name FROM district WHERE id_district = {id_district};""")
            res = self._cur.fetchone()
            if res:
                return res[0]
            return ""
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_parallel_by_id_oo_parallels(self, id_oo_parallels):
        try:
            self._cur.execute(f"SELECT parallel FROM oo_parallels WHERE id_oo_parallels = {id_oo_parallels}")
            res, = self._cur.fetchone()
            if res:
                return res
            return None
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_district_by_id_oo_parallels(self, id_oo_parallels):
        try:
            self._cur.execute(f"""
            SELECT district_name FROM district 
                WHERE id_district in 
                    (SELECT id_district FROM name_of_the_settlement 
                        WHERE id_name_of_the_settlement in 
                        (SELECT id_name_of_the_settlement FROM oo 
                            WHERE id_oo in (SELECT id_oo FROM oo_parallels WHERE id_oo_parallels = {id_oo_parallels})));
            """)
            res, = self._cur.fetchone()
            if res:
                return res.replace("_", " ")
            return None
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_district_by_id_oo(self, id_oo):
        try:
            self._cur.execute(f"""
            SELECT district_name FROM district 
            WHERE id_district in 
            (
                SELECT id_district FROM name_of_the_settlement 
                WHERE id_name_of_the_settlement in 
                (
                    SELECT id_name_of_the_settlement FROM oo 
                    WHERE id_oo = {id_oo}
                )
            );""")
            res, = self._cur.fetchone()
            if res:
                return res
            return None
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_schools_in_risk_for_oo(self, id_oo, id_subjects, parallel):
        try:
            id_oo_parallels = self.get_id_oo_parallels(parallel=parallel,
                                                       id_oo=id_oo)
            id_oo_parallels_subjects = self.get_id_oo_parallels_subjects(id_subjects=id_subjects,
                                                                         id_oo_parallels=id_oo_parallels)
            self._cur.execute(f"""
            SELECT id_oo_parallels, 
                max(mark_count) filter (where value = 2) as vpr_two, 
                max(mark_count) filter (where value = 3) as vpr_three, 
                max(mark_count) filter (where value = 4) as vpr_four, 
                max(mark_count) filter (where value = 5) as vpr_five, 
                l_s_two, l_s_three, l_s_four, l_s_five FROM 
        (SELECT id_oo_parallels, value, COUNT(value) as mark_count FROM
            (SELECT id_oo_parallels,sum_marks,
                CASE WHEN sum_marks<mark_three THEN 2
                    WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                    WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                    WHEN sum_marks>=mark_five THEN 5
                    ELSE 0
                END AS value
                FROM (SELECT id_students, id_oo_parallels, sum_marks, mark_three, mark_four, mark_five  
                FROM (SELECT id_students, id_oo_parallels, id_oo_parallels_subjects, SUM(mark) as sum_marks 
                    FROM result_for_task 
                    WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects} AND id_oo_parallels = {id_oo_parallels}
                    GROUP BY id_students, id_oo_parallels, id_oo_parallels_subjects) AS t1
                LEFT JOIN 
                    (SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five 
                    FROM oo_parallels_subjects 
                    WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects}) AS t2
                USING (id_oo_parallels_subjects)) AS t3)
            AS t4 GROUP BY value, id_oo_parallels ORDER BY (value)) AS vpr

        LEFT JOIN 
            (SELECT id_oo_parallels, 
                    max(mark_count_for_last_semester) filter (where mark_for_last_semester = 2) as l_s_two, 
                    max(mark_count_for_last_semester) filter (where mark_for_last_semester = 3) as l_s_three, 
                    max(mark_count_for_last_semester) filter (where mark_for_last_semester = 4) as l_s_four, 
                    max(mark_count_for_last_semester) filter (where mark_for_last_semester = 5) as l_s_five FROM 
            (SELECT id_oo_parallels, mark_for_last_semester, COUNT(mark_for_last_semester) AS mark_count_for_last_semester
                FROM (SELECT DISTINCT id_oo_parallels, id_students, id_oo_parallels_subjects, mark_for_last_semester 
                    FROM result_for_task 
                    WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects} AND id_oo_parallels = {id_oo_parallels}) 
                    AS t1 GROUP BY id_oo_parallels, mark_for_last_semester) AS t2 GROUP BY id_oo_parallels) AS l_s
            USING (id_oo_parallels)
             GROUP BY id_oo_parallels, l_s_two, l_s_three, l_s_four, l_s_five;""")
            res = self._cur.fetchone()
            if res:
                id_oo_parallels, vpr_two, vpr_three, vpr_four, vpr_five, l_s_two, l_s_three, l_s_four, l_s_five = res
                school_name = self.get_oo_name_from_oo_parallels(id_oo_parallels)
                district_name = self.get_district_by_id_oo_parallels(id_oo_parallels)

                vpr_two = vpr_two if vpr_two else 0
                vpr_three = vpr_three if vpr_three else 0
                vpr_four = vpr_four if vpr_four else 0
                vpr_five = vpr_five if vpr_five else 0

                l_s_two = l_s_two if l_s_two else 0
                l_s_three = l_s_three if l_s_three else 0
                l_s_four = l_s_four if l_s_four else 0
                l_s_five = l_s_five if l_s_five else 0

                vpr_results = {"2": vpr_two,
                               "3": vpr_three,
                               "4": vpr_four,
                               "5": vpr_five}

                last_semester_results = {"2": l_s_two,
                                         "3": l_s_three,
                                         "4": l_s_four,
                                         "5": l_s_five}

                return {"district_name": district_name,
                        "school_name": school_name,
                        "vpr_results": vpr_results,
                        "last_semester_results": last_semester_results,
                        "count_of_students": vpr_two + vpr_three + vpr_four + vpr_five}
            return {}
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_schools_in_risk_for_district(self, year, id_district, parallel, id_subjects):
        try:
            self._cur.execute(f"""
            SELECT id_oo, oo_name FROM oo 
            WHERE id_oo in 
            (
                SELECT id_oo FROM schools_in_risk 
                WHERE year = '{year}' 
                AND parallel = {parallel} 
                AND id_subjects = {id_subjects}  
                AND id_oo in 
                (
                    SELECT id_oo FROM oo 
                    WHERE id_name_of_the_settlement in 
                    (
                        SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                        WHERE id_district = {id_district}
                    )
                )
            )
            ;""")
            res = self._cur.fetchall()

            schools_array = {}
            if res:
                for id_oo, oo_name in res:
                    district_name = self.get_district_name(id_district)
                    if district_name not in schools_array:
                        schools_array[district_name] = [oo_name]
                    else:
                        schools_array[district_name].append(oo_name)

            return schools_array
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_schools_in_risk_for_all(self, year, parallel, id_subjects):
        try:
            self._cur.execute(f"""
            SELECT id_oo, oo_name FROM oo 
            WHERE id_oo in 
            (
                SELECT id_oo FROM schools_in_risk 
                WHERE year = '{year}' 
                AND parallel = {parallel} 
                AND id_subjects = {id_subjects}  
            )
            ;""")
            res = self._cur.fetchall()

            schools_array = {}
            if res:
                for id_oo, oo_name in res:
                    district_name = self.get_district_by_id_oo(id_oo)
                    if district_name not in schools_array:
                        schools_array[district_name.replace("_", " ")] = [oo_name]
                    else:
                        schools_array[district_name.replace("_", " ")].append(oo_name)

            return schools_array
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_task_description_for_all(self, id_subjects, parallel, year):
        try:
            self._cur.execute(f"""
            SELECT task_number, task_number_from_kim, fgos, poop_noo, max_mark, value, count FROM 
            (SELECT id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, max_mark, value, COUNT(value) as count FROM
            (SELECT id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number,task_number_from_kim, max_mark, 
                CASE WHEN mark = max_mark THEN 'Выполнили'
                    ELSE 'Не выполнили'
                END AS value FROM
            ((SELECT id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number, mark FROM result_for_task 
                WHERE id_oo_parallels_subjects IN 
                    (SELECT id_oo_parallels_subjects FROM oo_parallels_subjects 
                        WHERE id_oo_parallels IN 
                            (SELECT id_oo_parallels FROM oo_parallels 
                                WHERE parallel={parallel} AND id_oo in 
                                    (SELECT id_oo FROM oo 
                                        WHERE year='{year}'))
                        AND id_subjects={id_subjects}) GROUP BY id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number, mark) AS t1
            LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers,task_number_from_kim, max_mark FROM distributio_of_tasks_by_positions_of_codifiers 
                    WHERE id_subjects = {id_subjects} AND parallel = {parallel}) AS t2
                USING(id_distributio_of_tasks_by_positions_of_codifiers))) AS t3  group by id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, max_mark, value ORDER BY (task_number)) as t5
            LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers, fgos, poop_noo FROM distributio_of_tasks_by_positions_of_codifiers 
                    WHERE id_subjects = {id_subjects} AND parallel = {parallel}) AS t4 USING(id_distributio_of_tasks_by_positions_of_codifiers) 
                    group by task_number, task_number_from_kim, fgos, poop_noo, max_mark, value, count 
                    ORDER BY (task_number);""")
            res = self._cur.fetchall()
            res_dict = {}
            if res:
                for task_number, task_number_from_kim, fgos, poop_noo, max_mark, value, count in res:
                    if task_number not in res_dict:
                        text = f"{fgos.strip()}  {poop_noo.strip()}".replace("\n", " ").replace("_x0002_", "").replace(
                            "None", "")

                        res_dict[task_number] = {"task_number_from_kim": task_number_from_kim,
                                                 "text": text,
                                                 "max_mark": max_mark,
                                                 "values": {value: {"count": count, "%": 100}}}
                    else:
                        res_dict[task_number]["values"][value] = {"count": count}
                        all_stud = 0
                        for key, key_value in res_dict[task_number]["values"].items():
                            all_stud += res_dict[task_number]["values"][key]["count"]
                        for key, key_value in res_dict[task_number]["values"].items():
                            res_dict[task_number]["values"][key]["%"] = round(
                                (res_dict[task_number]["values"][key]["count"] / all_stud) * 100, 1)
                for task_number in res_dict:
                    if "Выполнили" not in res_dict[task_number]["values"]:
                        res_dict[task_number]["values"]["Выполнили"] = {"count": 0, "%": 0}

                    if "Не выполнили" not in res_dict[task_number]["values"]:
                        res_dict[task_number]["values"]["Не выполнили"] = {"count": 0, "%": 0}

            return res_dict
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_task_description_for_district(self, id_district, id_subjects, parallel, year):
        try:
            self._cur.execute(f"""
            SELECT task_number, task_number_from_kim, fgos, poop_noo, max_mark, value, count FROM 
            (SELECT id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, max_mark, value, COUNT(value) as count FROM
            (SELECT id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number,task_number_from_kim, max_mark, 
                CASE WHEN mark = max_mark THEN 'Выполнили'
                    ELSE 'Не выполнили'
                END AS value FROM
            ((SELECT id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number, mark FROM result_for_task 
                WHERE id_oo_parallels_subjects IN 
                    (SELECT id_oo_parallels_subjects FROM oo_parallels_subjects 
                        WHERE id_oo_parallels IN 
                            (SELECT id_oo_parallels FROM oo_parallels 
                                WHERE parallel={parallel} AND id_oo in 
                                    (SELECT id_oo FROM oo 
                                        WHERE year='{year}' AND id_name_of_the_settlement in (SELECT id_name_of_the_settlement FROM name_of_the_settlement WHERE id_district = {id_district})))
                        AND id_subjects={id_subjects}) GROUP BY id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number, mark) AS t1
            LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers,task_number_from_kim, max_mark FROM distributio_of_tasks_by_positions_of_codifiers 
                    WHERE id_subjects = {id_subjects} AND parallel = {parallel}) AS t2
                USING(id_distributio_of_tasks_by_positions_of_codifiers))) AS t3  group by id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, max_mark, value ORDER BY (task_number)) as t5
            LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers, fgos, poop_noo FROM distributio_of_tasks_by_positions_of_codifiers 
                    WHERE id_subjects = {id_subjects} AND parallel = {parallel}) AS t4 USING(id_distributio_of_tasks_by_positions_of_codifiers) group by task_number, task_number_from_kim, fgos, poop_noo, max_mark, value, count ORDER BY (task_number);
            """)
            res = self._cur.fetchall()
            res_dict = {}
            if res:
                for task_number, task_number_from_kim, fgos, poop_noo, max_mark, value, count in res:
                    if task_number not in res_dict:
                        text = f"{fgos.strip()}  {poop_noo.strip()}".replace("\n", " ").replace("_x0002_", "").replace(
                            "None", "")

                        res_dict[task_number] = {"task_number_from_kim": task_number_from_kim,
                                                 "text": text,
                                                 "max_mark": max_mark,
                                                 "values": {value: {"count": count, "%": 100}}}
                    else:
                        res_dict[task_number]["values"][value] = {"count": count}
                        all_stud = 0
                        for key, key_value in res_dict[task_number]["values"].items():
                            all_stud += res_dict[task_number]["values"][key]["count"]
                        for key, key_value in res_dict[task_number]["values"].items():
                            res_dict[task_number]["values"][key]["%"] = round(
                                (res_dict[task_number]["values"][key]["count"] / all_stud) * 100, 1)
                for task_number in res_dict:
                    if "Выполнили" not in res_dict[task_number]["values"]:
                        res_dict[task_number]["values"]["Выполнили"] = {"count": 0, "%": 0}

                    if "Не выполнили" not in res_dict[task_number]["values"]:
                        res_dict[task_number]["values"]["Не выполнили"] = {"count": 0, "%": 0}

            return res_dict
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_task_description_for_oo(self, id_oo_parallels_subjects):
        try:
            self._cur.execute(f"""
            SELECT task_number, task_number_from_kim, fgos, poop_noo, max_mark, value, count FROM 
            (SELECT id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, max_mark, value, COUNT(value) as count FROM
            (SELECT id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number,task_number_from_kim, max_mark, 
                CASE WHEN mark = max_mark THEN 'Выполнили'
                    ELSE 'Не выполнили'
                END AS value FROM
            ((SELECT id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number, mark FROM result_for_task 
                WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects}
                     GROUP BY id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number, mark) AS t1

            LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers,task_number_from_kim, max_mark FROM distributio_of_tasks_by_positions_of_codifiers 
                    WHERE id_subjects IN 
                    (SELECT id_subjects FROM oo_parallels_subjects 
                        WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects}) 
                    AND parallel IN 
                    (SELECT parallel FROM oo_parallels 
                        WHERE id_oo_parallels IN 
                        (SELECT id_oo_parallels FROM oo_parallels_subjects 
                            WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects}))) AS t2
                USING(id_distributio_of_tasks_by_positions_of_codifiers))) AS t3  
                group by id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, max_mark, value ORDER BY (task_number)) as t6

            LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers, fgos, poop_noo FROM distributio_of_tasks_by_positions_of_codifiers 
                    WHERE id_subjects IN 
                    (SELECT id_subjects FROM oo_parallels_subjects 
                        WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects})
                    AND parallel IN 
                    (SELECT parallel FROM oo_parallels 
                        WHERE id_oo_parallels IN 
                        (SELECT id_oo_parallels FROM oo_parallels_subjects 
                            WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects}))) AS T2
                USING(id_distributio_of_tasks_by_positions_of_codifiers) 
                group by task_number, task_number_from_kim, fgos, poop_noo, max_mark, value, count ORDER BY (task_number);""")
            res = self._cur.fetchall()
            res_dict = {}
            if res:
                for task_number, task_number_from_kim, fgos, poop_noo, max_mark, value, count in res:
                    if task_number not in res_dict:
                        text = f"{fgos.strip()}  {poop_noo.strip()}".replace("\n", " ").replace("_x0002_", "").replace(
                            "None", "")
                        res_dict[task_number] = {"task_number_from_kim": task_number_from_kim,
                                                 "text": text,
                                                 "max_mark": max_mark,
                                                 "values": {value: {"count": count, "%": 100}}}
                    else:
                        res_dict[task_number]["values"][value] = {"count": count}
                        all_stud = 0
                        for key, key_value in res_dict[task_number]["values"].items():
                            all_stud += res_dict[task_number]["values"][key]["count"]
                        for key, key_value in res_dict[task_number]["values"].items():
                            res_dict[task_number]["values"][key]["%"] = round(
                                (res_dict[task_number]["values"][key]["count"] / all_stud) * 100, 1)
                for task_number in res_dict:
                    if "Выполнили" not in res_dict[task_number]["values"]:
                        res_dict[task_number]["values"]["Выполнили"] = {"count": 0, "%": 0}

                    if "Не выполнили" not in res_dict[task_number]["values"]:
                        res_dict[task_number]["values"]["Не выполнили"] = {"count": 0, "%": 0}

            return res_dict
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_task_description_for_one_task_for_all(self, id_subjects, parallel, task_number, year):
        try:
            self._cur.execute(f"""
            SELECT id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, level, fgos, poop_noo, max_mark, value, count FROM 
            (SELECT id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, max_mark, value, COUNT(value) as count FROM
            (SELECT id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number,task_number_from_kim, max_mark, 
                CASE WHEN mark = max_mark THEN 'Выполнили'
                    ELSE 'Не выполнили'
                END AS value FROM
            ((SELECT id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number, mark FROM result_for_task 
                WHERE id_oo_parallels_subjects IN 
                    (SELECT id_oo_parallels_subjects FROM oo_parallels_subjects 
                        WHERE id_oo_parallels IN 
                            (SELECT id_oo_parallels FROM oo_parallels 
                                WHERE parallel={parallel} AND id_oo in 
                                    (SELECT id_oo FROM oo 
                                        WHERE year='{year}'))
                        AND id_subjects={id_subjects})
                    AND task_number = {task_number} GROUP BY id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number, mark) AS t1
            LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers,task_number_from_kim, max_mark FROM distributio_of_tasks_by_positions_of_codifiers 
                    WHERE id_subjects = {id_subjects} AND parallel = {parallel} AND task_number = {task_number}) AS t2
                USING(id_distributio_of_tasks_by_positions_of_codifiers))) AS t3  
                group by id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, max_mark, value ORDER BY (task_number)) as t5
            LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers, level, fgos, poop_noo FROM distributio_of_tasks_by_positions_of_codifiers 
                    WHERE id_subjects = {id_subjects} AND parallel = {parallel} AND task_number = {task_number}) AS t4 USING(id_distributio_of_tasks_by_positions_of_codifiers) 
                    group by id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, level, fgos, poop_noo, max_mark, value, count ORDER BY (task_number);
            """)
            res = self._cur.fetchall()
            res_dict = {}
            if res:
                for id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, lvl, fgos, poop_noo, max_mark, value, count in res:
                    if task_number not in res_dict:
                        text = f"{fgos.strip()}  {poop_noo.strip()}".replace("\n", " ").replace("_x0002_", "").replace(
                            "None", "")

                        res_dict[task_number] = {"task_number_from_kim": "Задание " + task_number_from_kim,
                                                 "text": text,
                                                 "max_mark": max_mark,
                                                 "values": {value: {"count": count, "%": 100}},
                                                 "kt": self.get_description_from_kt(
                                                     id_distributio_of_tasks_by_positions_of_codifiers),
                                                 "ks": self.get_description_from_ks(
                                                     id_distributio_of_tasks_by_positions_of_codifiers),
                                                 "level": lvl.replace("None", "")}
                    else:
                        res_dict[task_number]["values"][value] = {"count": count}
                        all_stud = 0
                        for key, key_value in res_dict[task_number]["values"].items():
                            all_stud += res_dict[task_number]["values"][key]["count"]
                        for key, key_value in res_dict[task_number]["values"].items():
                            res_dict[task_number]["values"][key]["%"] = round(
                                (res_dict[task_number]["values"][key]["count"] / all_stud) * 100, 1)
                for task_number in res_dict:
                    if "Выполнили" not in res_dict[task_number]["values"]:
                        res_dict[task_number]["values"]["Выполнили"] = {"count": 0, "%": 0}

                    if "Не выполнили" not in res_dict[task_number]["values"]:
                        res_dict[task_number]["values"]["Не выполнили"] = {"count": 0, "%": 0}

            return res_dict
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_task_description_for_one_task_for_district(self, id_district, id_subjects, parallel, task_number,
                                                       year):
        try:
            self._cur.execute(f"""
            SELECT id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, level, fgos, poop_noo, max_mark, value, count FROM 
            (SELECT id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, max_mark, value, COUNT(value) as count FROM
            (SELECT id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number,task_number_from_kim, max_mark, 
                CASE WHEN mark = max_mark THEN 'Выполнили'
                    ELSE 'Не выполнили'
                END AS value FROM
            ((SELECT id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number, mark FROM result_for_task 
                WHERE id_oo_parallels_subjects IN 
                    (SELECT id_oo_parallels_subjects FROM oo_parallels_subjects 
                        WHERE id_oo_parallels IN 
                            (SELECT id_oo_parallels FROM oo_parallels 
                                WHERE parallel={parallel} AND id_oo in 
                                    (SELECT id_oo FROM oo 
                                        WHERE year='{year}' AND id_name_of_the_settlement in 
                                            (SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                                                WHERE id_district = {id_district})))
                        AND id_subjects={id_subjects})
                    AND task_number = {task_number} GROUP BY id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number, mark) AS t1
            LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers,task_number_from_kim, max_mark FROM distributio_of_tasks_by_positions_of_codifiers 
                    WHERE id_subjects = {id_subjects} AND parallel = {parallel} AND task_number = {task_number}) AS t2
                USING(id_distributio_of_tasks_by_positions_of_codifiers))) AS t3  
                group by id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, max_mark, value ORDER BY (task_number)) as t5
            LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers, level, fgos, poop_noo FROM distributio_of_tasks_by_positions_of_codifiers 
                    WHERE id_subjects = {id_subjects} AND parallel = {parallel} AND task_number = {task_number}) AS t4 USING(id_distributio_of_tasks_by_positions_of_codifiers) 
                    group by id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, level, fgos, poop_noo, max_mark, value, count ORDER BY (task_number);
            """)
            res = self._cur.fetchall()
            res_dict = {}
            if res:
                for id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, lvl, fgos, poop_noo, max_mark, value, count in res:
                    if task_number not in res_dict:
                        text = f"{fgos.strip()}  {poop_noo.strip()}".replace("\n", " ").replace("_x0002_", "").replace(
                            "None", "")

                        res_dict[task_number] = {"task_number_from_kim": "Задание " + task_number_from_kim,
                                                 "text": text,
                                                 "max_mark": max_mark,
                                                 "values": {value: {"count": count, "%": 100}},
                                                 "kt": self.get_description_from_kt(
                                                     id_distributio_of_tasks_by_positions_of_codifiers),
                                                 "ks": self.get_description_from_ks(
                                                     id_distributio_of_tasks_by_positions_of_codifiers),
                                                 "level": lvl.replace("None", "")}
                    else:
                        res_dict[task_number]["values"][value] = {"count": count}
                        all_stud = 0
                        for key, key_value in res_dict[task_number]["values"].items():
                            all_stud += res_dict[task_number]["values"][key]["count"]
                        for key, key_value in res_dict[task_number]["values"].items():
                            res_dict[task_number]["values"][key]["%"] = round(
                                (res_dict[task_number]["values"][key]["count"] / all_stud) * 100, 1)
                for task_number in res_dict:
                    if "Выполнили" not in res_dict[task_number]["values"]:
                        res_dict[task_number]["values"]["Выполнили"] = {"count": 0, "%": 0}

                    if "Не выполнили" not in res_dict[task_number]["values"]:
                        res_dict[task_number]["values"]["Не выполнили"] = {"count": 0, "%": 0}

            return res_dict
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_task_description_for_one_task_for_oo(self, id_oo_parallels_subjects, task_number):
        try:
            self._cur.execute(f"""
            SELECT id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, level, fgos, poop_noo, max_mark, value, count FROM 
            (SELECT id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, max_mark, value, COUNT(value) as count FROM
            (SELECT id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number,task_number_from_kim, max_mark, 
                CASE WHEN mark = max_mark THEN 'Выполнили'
                    ELSE 'Не выполнили'
                END AS value FROM
            ((SELECT id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number, mark FROM result_for_task 
                WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects} AND task_number = {task_number}
                     GROUP BY id_result_for_task, id_distributio_of_tasks_by_positions_of_codifiers, task_number, mark) AS t1

            LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers,task_number_from_kim, max_mark FROM distributio_of_tasks_by_positions_of_codifiers 
                    WHERE id_subjects IN 
                    (SELECT id_subjects FROM oo_parallels_subjects 
                        WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects}) 
                    AND parallel IN 
                    (SELECT parallel FROM oo_parallels 
                        WHERE id_oo_parallels IN 
                        (SELECT id_oo_parallels FROM oo_parallels_subjects 
                            WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects}))
                    AND task_number = {task_number}) AS t2
                USING(id_distributio_of_tasks_by_positions_of_codifiers))) AS t3  
                group by id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, max_mark, value ORDER BY (task_number)) as t6

            LEFT JOIN (SELECT id_distributio_of_tasks_by_positions_of_codifiers, level, fgos, poop_noo FROM distributio_of_tasks_by_positions_of_codifiers 
                    WHERE id_subjects IN 
                    (SELECT id_subjects FROM oo_parallels_subjects 
                        WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects})
                    AND parallel IN 
                    (SELECT parallel FROM oo_parallels 
                        WHERE id_oo_parallels IN 
                        (SELECT id_oo_parallels FROM oo_parallels_subjects 
                            WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects}))
                    AND task_number = {task_number}) AS T2
                USING(id_distributio_of_tasks_by_positions_of_codifiers) group by id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, level, fgos, poop_noo, max_mark, value, count ORDER BY (task_number);
            """)
            res = self._cur.fetchall()
            res_dict = {}
            if res:
                for id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, lvl, fgos, poop_noo, max_mark, value, count in res:
                    if task_number not in res_dict:
                        text = f"{fgos.strip()}  {poop_noo.strip()}".replace("\n", " ").replace("_x0002_", "").replace(
                            "None", "")

                        res_dict[task_number] = {"task_number_from_kim": "Задание " + task_number_from_kim,
                                                 "text": text,
                                                 "max_mark": max_mark,
                                                 "values": {value: {"count": count, "%": 100}},
                                                 "kt": self.get_description_from_kt(
                                                     id_distributio_of_tasks_by_positions_of_codifiers),
                                                 "ks": self.get_description_from_ks(
                                                     id_distributio_of_tasks_by_positions_of_codifiers),
                                                 "level": lvl.replace("None", "")}
                    else:
                        res_dict[task_number]["values"][value] = {"count": count}
                        all_stud = 0
                        for key, key_value in res_dict[task_number]["values"].items():
                            all_stud += res_dict[task_number]["values"][key]["count"]
                        for key, key_value in res_dict[task_number]["values"].items():
                            res_dict[task_number]["values"][key]["%"] = round(
                                (res_dict[task_number]["values"][key]["count"] / all_stud) * 100, 1)
                for task_number in res_dict:
                    if "Выполнили" not in res_dict[task_number]["values"]:
                        res_dict[task_number]["values"]["Выполнили"] = {"count": 0, "%": 0}

                    if "Не выполнили" not in res_dict[task_number]["values"]:
                        res_dict[task_number]["values"]["Не выполнили"] = {"count": 0, "%": 0}

            return res_dict
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_description_from_ks(self, id_distributio_of_tasks_by_positions_of_codifiers):
        try:
            self._cur.execute(
                f'''SELECT description as "Проверяемые элементы содержания" from ks 
                        WHERE id_ks in 
                            (select distinct id_ks from ks_kt 
                                WHERE id_distributio_of_tasks_by_positions_of_codifiers = {id_distributio_of_tasks_by_positions_of_codifiers});''')
            res = self._cur.fetchall()

            if res:
                if len(res) > 1:
                    return [x[0] for x in res if x[0].replace("None", "") != ""]
                else:
                    return [x[0].replace("None", "") for x in res]

            return []
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_description_from_kt(self, id_distributio_of_tasks_by_positions_of_codifiers):
        try:
            self._cur.execute(
                f'''SELECT description as "Проверяемые элементы содержания" from kt 
                        WHERE id_kt in 
                            (select distinct id_kt from ks_kt 
                                WHERE id_distributio_of_tasks_by_positions_of_codifiers = {id_distributio_of_tasks_by_positions_of_codifiers});''')
            res = self._cur.fetchall()

            if res:
                if len(res) > 1:
                    return [x[0] for x in res if x[0].replace("None", "") != ""]
                else:
                    return [x[0].replace("None", "") for x in res]

            return []

        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_task_number_from_kim(self, id_subjects, parallel, year):
        try:
            self._cur.execute(
                f"SELECT task_number, task_number_from_kim FROM distributio_of_tasks_by_positions_of_codifiers "
                f"WHERE id_subjects = {id_subjects} "
                f"AND parallel = {parallel} "
                f"AND year='{year}' order by (task_number);")
            res = self._cur.fetchall()

            if res:
                return res
            return []
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_task_number_from_kim_by_id_oo_parallels_subjects(self, id_oo_parallels_subjects):
        try:
            self._cur.execute(
                f"""
                SELECT task_number, task_number_from_kim FROM distributio_of_tasks_by_positions_of_codifiers 
                WHERE id_subjects IN 
                    (
                        SELECT id_subjects FROM oo_parallels_subjects WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects}
                    )
                AND parallel IN 
                    (
                        SELECT parallel FROM oo_parallels 
                        WHERE id_oo_parallels IN 
                            (
                                SELECT id_oo_parallels FROM oo_parallels_subjects 
                                WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects}
                            )
                    ) order by (task_number);""")
            res = self._cur.fetchall()

            if res:
                return res
            return []
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_max_mark(self, subject_name, parallel, task_number_from_kim):
        self._cur.execute(f"""
            select max_mark from distributio_of_tasks_by_positions_of_codifiers 
                where id_subjects = {self.get_subject_id(subject_name=subject_name)} 
                and parallel = {parallel} 
                and task_number_from_kim = '{task_number_from_kim}'""")
        res = self._cur.fetchone()
        if res:
            return res[0]
        return

    def get_task_number(self, task_number_from_kim, id_subjects, parallel):
        self._cur.execute(f"""
            select task_number from distributio_of_tasks_by_positions_of_codifiers 
                where task_number_from_kim = '{task_number_from_kim}' 
                and id_subjects = {id_subjects} and parallel = {parallel};
        """)
        res = self._cur.fetchone()
        if res:
            return res[0]
        return
