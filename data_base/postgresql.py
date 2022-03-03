import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Postgresql:
    def __init__(self, connection):
        self.connection = connection
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self._cur = self.connection.cursor()

    def get_user(self, id_user):
        try:
            self._cur.execute(f"""
            SELECT * FROM users 
            WHERE id_user = {id_user} 
            LIMIT 1;""")
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
            self._cur.execute(f"""
            SELECT * FROM users 
            WHERE login = '{login}' 
            LIMIT 1;""")
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
            self._cur.execute(f"UPDATE users SET avatar = {binary} WHERE id_user = {user_id};")
        except psycopg2.Error as e:
            print("Ошибка обновления аватара в БД: " + str(e))
            return False
        return True

    def get_count_students(self, year):
        try:
            self._cur.execute(f"""
            SELECT COUNT(*) AS count_row FROM students 
            WHERE id_oo_parallels IN 
            (
                SELECT id_oo_parallels FROM oo_parallels 
                WHERE id_oo IN 
                (
                    SELECT id_oo FROM oo 
                    WHERE year = '{year}'
                )
            );""")
            res, = self._cur.fetchone()
            if res:
                return res
            return 0
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_count_oo(self, year="2021"):
        try:
            self._cur.execute(f"""
            SELECT COUNT(*) FROM oo 
            WHERE year = '{year}';""")
            res, = self._cur.fetchone()
            if res:
                return res
            return 0
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_count_of_subject(self):
        try:
            self._cur.execute(f"SELECT COUNT(*) AS count_row FROM subjects;")
            res, = self._cur.fetchone()
            if res:
                return res
            return 0
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_count_of_parallels(self):
        try:
            self._cur.execute(f"SELECT COUNT(*) AS count_row FROM parallels;")
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
                    SELECT id_oo FROM oo 
                    WHERE year = '{year}'
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
            self._cur.execute(f"""
            SELECT parallel FROM oo_parallels 
            WHERE id_oo = {id_oo};""")
            res = self._cur.fetchall()
            if res:
                return res
        except psycopg2.Error as e:
            print("Ошибка получения статей из БД " + str(e))
        return []

    def get_subject_id(self, subject_name):
        try:
            self._cur.execute(
                f"""
                SELECT id_subjects FROM subjects 
                WHERE subject_name = '{subject_name.replace(' ', '_')}';""")
            res, = self._cur.fetchone()
            if res:
                return res
        except psycopg2.Error as e:
            print("Ошибка получения статей из БД " + str(e))
            return []

    def get_subject_name(self, id_subjects):

        try:
            if id_subjects:
                self._cur.execute(f"""
                SELECT subject_name FROM subjects
                WHERE id_subjects = {id_subjects};""")
                res = self._cur.fetchone()
                if res:
                    return res[0].replace("_", " ")
                return ""
        except psycopg2.Error as e:
            print("Ошибка получения статей из БД " + str(e))

    def get_subjects_for_oo(self, oo_login, parallel, id_user, year):
        try:
            self._cur.execute(f"""
            SELECT id_subjects, subject_name FROM subjects 
            WHERE id_subjects in 
            (
                SELECT id_subjects FROM oo_parallels_subjects 
                WHERE id_oo_parallels in 
                (
                    SELECT id_oo_parallels FROM oo_parallels 
                    WHERE parallel = {parallel} 
                    AND id_oo in 
                    (
                        SELECT id_oo FROM oo 
                        WHERE year='{year}' 
                        AND oo_login = '{oo_login}'
                        AND oo_login in 
                        (
                            SELECT oo_login FROM users_oo_logins 
                            WHERE id_user = {id_user}
                        )
                    )
                )
            );""")
            res = self._cur.fetchall()
            if res:
                return [[id_subjects, subject_name.replace("_", " ")] for id_subjects, subject_name in res]
            return []
        except psycopg2.Error as e:
            print("Ошибка получения статей из БД " + str(e))
        return []

    def get_id_oo(self, oo_login, year):
        try:
            self._cur.execute(
                f"""
                SELECT id_oo FROM oo 
                WHERE oo_login = '{oo_login}' 
                AND year = '{year}';""")
            res, = self._cur.fetchone()
            if not res:
                print("id_oo не был найден")
                return None
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_oo_parallels(self, parallel, id_oo):
        try:
            self._cur.execute(
                f"""
                SELECT id_oo_parallels FROM oo_parallels 
                WHERE parallel = {parallel} 
                AND id_oo = {id_oo};""")
            res, = self._cur.fetchone()
            if not res:
                print("id_oo_parallels не был найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_oo_parallels_subjects(self, id_subjects, id_oo_parallels):
        try:
            self._cur.execute(f"""
            SELECT id_oo_parallels_subjects FROM oo_parallels_subjects 
            WHERE id_oo_parallels = {id_oo_parallels} 
            AND id_subjects = {id_subjects};""")
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
                );""")
            res = self._cur.fetchall()
            if res:
                return [[x[0], x[1].replace("_", " ")] for x in res]
            return []
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_parallels(self, id_user, id_district, year):
        try:
            self._cur.execute(f"""
            SELECT DISTINCT parallel FROM oo_parallels WHERE id_oo in 
            (
                SELECT id_oo FROM oo 
                WHERE year = '{year}' 
                AND oo_login in 
                (
                    SELECT oo_login FROM users_oo_logins 
                    WHERE id_user = {id_user}
                )
                AND id_name_of_the_settlement IN 
                (
                    SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                    WHERE id_district = {id_district}
                ) 
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
            WHERE year = '{year}' 
            AND id_oo NOT IN 
            (
                SELECT id_oo FROM oo_levels_of_the_educational_program 
                WHERE id_levels_of_the_educational_program = 4 AND value = 'Да'
            ) 
            AND id_name_of_the_settlement IN 
            (
                SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                WHERE id_district = {id_district}
            ) 
            AND id_oo IN 
            (
                SELECT id_oo FROM oo_parallels
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

    def get_oo_from_id_oo_parallels_subjects(self, id_district, id_user, parallel, id_subjects):
        try:
            self._cur.execute(f"""
            SELECT id_oo_parallels_subjects, id_oo_parallels FROM oo_parallels_subjects 
            WHERE id_subjects = {id_subjects} 
            AND id_oo_parallels in 
            (
                SELECT id_oo_parallels FROM oo_parallels 
                WHERE parallel = {parallel} 
                AND id_oo in 
                (
                    SELECT id_oo FROM oo 
                    WHERE id_oo NOT IN 
                    (
                        SELECT id_oo FROM oo_levels_of_the_educational_program 
                        WHERE id_levels_of_the_educational_program = 4 
                        AND value = 'Да'
                    ) 
                    AND id_name_of_the_settlement IN 
                    (
                        SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                        WHERE id_district = {id_district}
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
            return []

        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_oo_name_from_oo_parallels(self, id_oo_parallels):
        try:
            self._cur.execute(f"""
            SELECT oo_name FROM oo 
            WHERE id_oo in 
            (
                SELECT id_oo FROM oo_parallels 
                WHERE id_oo_parallels = {id_oo_parallels}
            );""")
            res, = self._cur.fetchone()
            if res:
                return res
            return ""
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_school_login(self, id_oo):
        try:
            self._cur.execute(f"""
            SELECT oo_login FROM oo 
            WHERE id_oo = {id_oo};""")
            res, = self._cur.fetchone()
            if res:
                return res
            return []
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_district_name(self, id_district):
        try:
            self._cur.execute(f"""
            SELECT district_name FROM district 
            WHERE id_district = {id_district};""")
            res = self._cur.fetchone()
            if res:
                return res[0]
            return ""
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_parallel_by_id_oo_parallels(self, id_oo_parallels):
        try:
            self._cur.execute(f"""
            SELECT parallel FROM oo_parallels 
            WHERE id_oo_parallels = {id_oo_parallels};""")
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
            (
                SELECT id_district FROM name_of_the_settlement 
                WHERE id_name_of_the_settlement in 
                (
                    SELECT id_name_of_the_settlement FROM oo 
                    WHERE id_oo in 
                    (
                        SELECT id_oo FROM oo_parallels 
                        WHERE id_oo_parallels = {id_oo_parallels}
                    )
                )
            );""")
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

    def get_description_from_ks(self, id_distributio_of_tasks_by_positions_of_codifiers):
        try:
            self._cur.execute(
                f'''SELECT description as "Проверяемые элементы содержания" FROM ks 
                    WHERE id_ks in 
                    (
                        SELECT distinct id_ks FROM ks_kt 
                        WHERE id_distributio_of_tasks_by_positions_of_codifiers = {id_distributio_of_tasks_by_positions_of_codifiers}
                    );''')
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
                f'''SELECT description as "Проверяемые элементы содержания" FROM kt 
                    WHERE id_kt in 
                    (
                        SELECT distinct id_kt FROM ks_kt 
                        WHERE id_distributio_of_tasks_by_positions_of_codifiers = {id_distributio_of_tasks_by_positions_of_codifiers}
                    );''')
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
                f"""
                SELECT task_number, task_number_from_kim FROM distributio_of_tasks_by_positions_of_codifiers 
                WHERE id_subjects = {id_subjects} 
                AND parallel = {parallel} 
                AND year = '{year}' 
                ORDER BY (task_number);""")
            res = self._cur.fetchall()

            if res:
                return res
            return []
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_task_number_from_kim_by_id_oo_parallels_subjects(self, year, oo_login, parallel, id_subjects):
        try:
            if oo_login != "all":
                id_oo = self.get_id_oo(oo_login=oo_login,
                                       year=year)
                id_oo_parallels = self.get_id_oo_parallels(parallel=parallel,
                                                           id_oo=id_oo)
                id_oo_parallels_subjects = self.get_id_oo_parallels_subjects(id_subjects=id_subjects,
                                                                             id_oo_parallels=id_oo_parallels)
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
                        ) 
                    AND task_number in 
                    (
                        SELECT task_number FROM result_for_task 
                        WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects} 
                        AND id_oo_parallels = {id_oo_parallels} 
                        AND id_subjects = {id_subjects}
                    )
                    AND year = '{year}'
                    ORDER BY (task_number);""")
            else:
                self._cur.execute(
                    f"""
                    SELECT task_number, task_number_from_kim FROM distributio_of_tasks_by_positions_of_codifiers 
                    WHERE id_subjects = {id_subjects} 
                    AND parallel = {parallel} 
                    AND year = '{year}' 
                    AND task_number in 
                    (
                        SELECT distinct task_number FROM result_for_task 
                        WHERE id_oo_parallels_subjects IN 
                        (
                            SELECT id_oo_parallels_subjects FROM oo_parallels_subjects 
                            WHERE id_subjects = {id_subjects} 
                            AND id_oo_parallels IN 
                            (
                                SELECT id_oo_parallels FROM oo_parallels 
                                WHERE parallel = {parallel} 
                                AND id_oo IN 
                                (
                                    SELECT id_oo FROM oo 
                                    WHERE year = '{year}'
                                )
                            )
                        )
                        AND id_oo_parallels IN
                        (
                            SELECT id_oo_parallels FROM oo_parallels 
                            WHERE parallel = {parallel} 
                            AND id_oo IN 
                            (
                                SELECT id_oo FROM oo 
                                WHERE year = '{year}'
                            )
                        )
                        AND id_subjects = {id_subjects} 
                    )
                    ORDER BY (task_number);""")

            res = self._cur.fetchall()

            if res:
                return res
            return []
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_max_mark(self, subject_name, parallel, task_number_from_kim):
        self._cur.execute(f"""
            SELECT max_mark FROM distributio_of_tasks_by_positions_of_codifiers 
            WHERE id_subjects = {self.get_subject_id(subject_name=subject_name)} 
            AND parallel = {parallel} 
            AND task_number_from_kim = '{task_number_from_kim}';""")
        res = self._cur.fetchone()
        if res:
            return res[0]
        return

    def get_task_number(self, task_number_from_kim, id_subjects, parallel):
        self._cur.execute(f"""
            SELECT task_number FROM distributio_of_tasks_by_positions_of_codifiers 
            WHERE task_number_from_kim = '{task_number_from_kim}' 
            AND id_subjects = {id_subjects} 
            AND parallel = {parallel};""")
        res = self._cur.fetchone()
        if res:
            return res[0]
        return

    def get_years(self, id_user):
        try:
            self._cur.execute(f"""
            SELECT DISTINCT year FROM oo 
            WHERE oo_login in 
            (
                SELECT oo_login FROM users_oo_logins 
                WHERE id_user = {id_user}
            )
            AND id_oo IN 
            (
               SELECT id_oo FROM oo_parallels
            );""")
            res = self._cur.fetchall()
            if res:
                return res
            return []
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def school_in_risk_access(self, id_user):
        try:
            self._cur.execute(f"""
            SELECT COUNT(*) FROM users_oo_logins 
            WHERE id_user = {id_user} 
            AND oo_login IN 
            (
                SELECT oo_login FROM oo 
                WHERE id_oo IN 
                (
                    SELECT id_oo FROM schools_in_risk
                )
            );""")
            res, = self._cur.fetchone()
            if res:
                return True
            return False
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))
