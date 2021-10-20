import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Postgresql:
    def __init__(self, connection):
        self.connection = connection
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self._cur = self.connection.cursor()

    def get_guest_menu(self):
        sql = '''SELECT * FROM guestmenu'''
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def get_logged_menu(self):
        sql = '''SELECT * FROM loggedmenu'''
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def get_admin_menu(self):
        sql = '''SELECT * FROM adminmenu'''
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def get_user(self, user_id):
        try:
            self._cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
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
            self._cur.execute(f"UPDATE users SET avatar = {binary} WHERE id = {user_id}")
        except psycopg2.Error as e:
            print("Ошибка обновления аватара в БД: " + str(e))
            return False
        return True

    def get_parallels_for_oo(self, id_oo):
        try:
            self._cur.execute(f"SELECT id_oo_parallels, parallel FROM oo_parallels WHERE id_oo = {id_oo}")
            res = self._cur.fetchall()
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
                    return res
        except psycopg2.Error as e:
            print("Ошибка получения статей из БД " + str(e))
        return []

    def get_subjects_for_oo_parallels(self, id_oo_parallels):
        try:
            if id_oo_parallels:
                self._cur.execute(f"SELECT id_oo_parallels_subjects, id_subjects FROM oo_parallels_subjects"
                                  f" WHERE id_oo_parallels = {id_oo_parallels}")
                res = self._cur.fetchall()
                if res:
                    return [[x[0], self.get_subject_name(x[1])[0].replace("_", " ")] for x in res]

        except psycopg2.Error as e:
            print("Ошибка получения статей из БД " + str(e))
        return []

    def get_districts(self):
        try:
            self._cur.execute(
                f'SELECT id_district, district_name FROM district ORDER BY id_district')
            res = self._cur.fetchall()
            if res:
                return res
        except psycopg2.Error as e:
            print("Ошибка получения муниципалитетов из БД " + str(e))
        return []

    def get_oo_from_district(self, id_district):
        try:
            self._cur.execute(f"""
            SELECT id_oo, oo_name 
            FROM oo 
            WHERE id_oo NOT IN 
                (SELECT id_oo 
                FROM oo_levels_of_the_educational_program 
                WHERE id_levels_of_the_educational_program = 4 AND value = 'Да') 
            AND id_name_of_the_settlement IN 
                (SELECT id_name_of_the_settlement 
                FROM name_of_the_settlement 
                WHERE id_district = {id_district}) 
            AND id_oo IN (SELECT id_oo FROM oo_parallels);""")
            res = self._cur.fetchall()
            if res:
                return res
            return []

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
                                                2)}}, count_of_all_students

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