import psycopg2
from data_base.postgresql import Postgresql


class DataBaseSchoolsInRisk(Postgresql):
    def __init__(self, connection):
        super().__init__(connection)

    def get_years(self, id_user):
        try:
            self._cur.execute(f"""
            SELECT DISTINCT year FROM schools_in_risk 
            WHERE id_oo in 
            (
                SELECT id_oo FROM oo 
                WHERE oo_login in 
                (
                    SELECT oo_login FROM users_oo_logins 
                    WHERE id_user = {id_user}
                )
            );""")

            res = self._cur.fetchall()
            if res:
                return res
            return []
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_districts(self, id_user, year):
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
            return []
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_oo_by_district(self, year, id_district, id_user):

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

    def get_parallels(self, year, id_district, id_oo):
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

    def get_subjects(self, year, id_district, id_oo, parallel):
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
                );""")

            else:
                self._cur.execute(f"""
                SELECT DISTINCT id_subjects FROM schools_in_risk 
                WHERE year = '{year}' 
                AND parallel = {parallel}
                AND id_oo = {id_oo};""")
            res = self._cur.fetchall()
            if res:
                return [(x[0], self.get_subject_name(id_subjects=x[0])) for x in res]
            return []
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
            );""")
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
            );""")
            res = self._cur.fetchall()

            schools_array = {}
            if res:
                for id_oo, oo_name in res:
                    district_name = self.get_district_name(id_district)
                    if district_name not in schools_array:
                        schools_array[district_name.replace("_", " ")] = [oo_name]
                    else:
                        schools_array[district_name.replace("_", " ")].append(oo_name)

            return schools_array
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
            (
                SELECT id_oo_parallels, value, COUNT(value) as mark_count FROM
                (
                    SELECT id_oo_parallels,sum_marks,
                    CASE 
                    WHEN sum_marks<mark_three THEN 2
                    WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                    WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                    WHEN sum_marks>=mark_five THEN 5
                    ELSE 0
                    END AS value FROM 
                    (
                        SELECT id_students, id_oo_parallels, sum_marks, mark_three, mark_four, mark_five FROM 
                        (
                            SELECT id_students, id_oo_parallels, id_oo_parallels_subjects, SUM(mark) as sum_marks FROM result_for_task 
                            WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects} 
                            AND id_oo_parallels = {id_oo_parallels}
                            GROUP BY id_students, id_oo_parallels, id_oo_parallels_subjects
                        ) AS t1
                        LEFT JOIN 
                        (
                            SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five FROM oo_parallels_subjects 
                            WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects}
                        ) AS t2 
                        USING (id_oo_parallels_subjects)
                    ) AS t3
                ) AS t4 GROUP BY value, id_oo_parallels ORDER BY (value)
            ) AS vpr 
            LEFT JOIN 
            (
                SELECT id_oo_parallels, 
                max(mark_count_for_last_semester) filter (where mark_for_last_semester = 2) as l_s_two, 
                max(mark_count_for_last_semester) filter (where mark_for_last_semester = 3) as l_s_three, 
                max(mark_count_for_last_semester) filter (where mark_for_last_semester = 4) as l_s_four, 
                max(mark_count_for_last_semester) filter (where mark_for_last_semester = 5) as l_s_five FROM 
                (
                    SELECT id_oo_parallels, mark_for_last_semester, COUNT(mark_for_last_semester) AS mark_count_for_last_semester FROM 
                    (
                        SELECT DISTINCT id_oo_parallels, id_students, id_oo_parallels_subjects, mark_for_last_semester FROM result_for_task 
                        WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects} 
                        AND id_oo_parallels = {id_oo_parallels} 
                    ) AS t1 GROUP BY id_oo_parallels, mark_for_last_semester 
                ) AS t2 GROUP BY id_oo_parallels 
            ) AS l_s 
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

                return {"district_name": district_name.replace("_", " "),
                        "school_name": school_name,
                        "vpr_results": vpr_results,
                        "last_semester_results": last_semester_results,
                        "count_of_students": vpr_two + vpr_three + vpr_four + vpr_five}
            return {}
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))
