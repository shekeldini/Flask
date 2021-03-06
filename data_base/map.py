import psycopg2
from data_base.classDataBaseResultVpr import DataBaseResultVpr


class Map(DataBaseResultVpr):
    def __init__(self, connection):
        super().__init__(connection)

    def get_mean_mark_for_district(self, id_district, id_subjects, parallel, year):
        try:
            self._cur.execute(f"""
            SELECT value, COUNT(value) FROM
            (
                SELECT id_students,sum_marks,
                CASE 
                WHEN sum_marks<mark_three THEN 2
                WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                WHEN sum_marks>=mark_five THEN 5
                ELSE 0
                END AS value FROM 
                (
                    SELECT id_students, sum_marks, mark_three, mark_four, mark_five FROM 
                    (
                        (
                            SELECT id_students, id_oo_parallels_subjects, SUM(mark) as sum_marks FROM result_for_task 
                            WHERE id_subjects={id_subjects} AND id_oo_parallels_subjects IN 
                            (
                                SELECT id_oo_parallels_subjects FROM oo_parallels_subjects 
                                WHERE id_oo_parallels IN 
                                (
                                    SELECT id_oo_parallels FROM oo_parallels 
                                    WHERE parallel={parallel} 
                                    AND id_oo in 
                                    (
                                        SELECT id_oo FROM oo 
                                        WHERE year='{year}'
                                        AND id_name_of_the_settlement in 
                                        (
                                            SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                                            WHERE id_district = {id_district}
                                        )
                                    )
                                )
                            ) GROUP BY id_students, id_oo_parallels_subjects
                        ) AS t1
                        LEFT JOIN 
                        (
                            SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five FROM oo_parallels_subjects 
                            WHERE id_subjects={id_subjects} AND id_oo_parallels IN 
                            (
                                SELECT id_oo_parallels FROM oo_parallels 
                                WHERE parallel={parallel} 
                                AND id_oo in 
                                (
                                    SELECT id_oo FROM oo 
                                    WHERE year='{year}'
                                    AND id_name_of_the_settlement in 
                                    (
                                        SELECT id_name_of_the_settlement FROM name_of_the_settlement 
                                        WHERE id_district = {id_district}
                                    )
                                )
                            )
                        ) AS t2 
                        USING (id_oo_parallels_subjects)
                    )
                ) AS t3
            ) AS t4 
            GROUP BY value ORDER BY (value);""")
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
                mean = round(((2 * count_of_mark_two + 3 * count_of_mark_three + 4 * count_of_mark_four + 5 * count_of_mark_five) / count_of_all_mark),1)

                return mean
            return

        except psycopg2.Error as e:
            print("???????????? ?????????????????? ???????????? ???? ???? " + str(e))

    def get_mean_mark_for_oo(self, oo_login, id_subjects, parallel, year):
        try:
            self._cur.execute(f"""
            SELECT value, COUNT(value) FROM
            (
                SELECT id_students,sum_marks,
                CASE 
                WHEN sum_marks<mark_three THEN 2
                WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                WHEN sum_marks>=mark_five THEN 5
                ELSE 0
                END AS value FROM 
                (
                    SELECT id_students, sum_marks, mark_three, mark_four, mark_five FROM 
                    (
                        (
                            SELECT id_students, id_oo_parallels_subjects, SUM(mark) as sum_marks FROM result_for_task 
                            WHERE id_subjects={id_subjects} AND id_oo_parallels_subjects IN 
                            (
                                SELECT id_oo_parallels_subjects FROM oo_parallels_subjects 
                                WHERE id_oo_parallels IN 
                                (
                                    SELECT id_oo_parallels FROM oo_parallels 
                                    WHERE parallel={parallel} 
                                    AND id_oo in 
                                    (
                                        SELECT id_oo FROM oo 
                                        WHERE year='{year}'
                                        AND oo_login = '{oo_login}'
                                    )
                                )
                            ) GROUP BY id_students, id_oo_parallels_subjects
                        ) AS t1
                        LEFT JOIN 
                        (
                            SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five FROM oo_parallels_subjects 
                            WHERE id_subjects={id_subjects} AND id_oo_parallels IN 
                            (
                                SELECT id_oo_parallels FROM oo_parallels 
                                WHERE parallel={parallel} 
                                AND id_oo in 
                                (
                                    SELECT id_oo FROM oo 
                                    WHERE year='{year}'
                                    AND oo_login = '{oo_login}'
                                )
                            )
                        ) AS t2 
                        USING (id_oo_parallels_subjects)
                    )
                ) AS t3
            ) AS t4 
            GROUP BY value ORDER BY (value);""")
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
                mean = round(((2 * count_of_mark_two + 3 * count_of_mark_three + 4 * count_of_mark_four + 5 * count_of_mark_five) / count_of_all_mark),1)

                return mean
            return
        except psycopg2.Error as e:
            print("???????????? ?????????????????? ???????????? ???? ???? " + str(e))

    def get_parallels_by_year(self, years: list):
        try:
            last_year = years.pop()
            query = f"""
            SELECT DISTINCT parallel FROM oo_parallels WHERE id_oo in 
            (
                SELECT id_oo FROM oo 
                WHERE year = '{last_year}' 
            ) """
            if years:
                for year in years:
                    query += f"""
                    INTERSECT
                    SELECT DISTINCT parallel FROM oo_parallels WHERE id_oo in 
                    (
                        SELECT id_oo FROM oo 
                        WHERE year = '{year}' 
                    ) """
            query += ";"
            self._cur.execute(query)
            res = self._cur.fetchall()
            if res:
                return res
            return []
        except psycopg2.Error as e:
            print("???????????? ?????????????????? ???????????? ???? ???? " + str(e))

    def get_all_subjects(self, parallel, id_district, years):
        try:
            if id_district != "all":
                last_year = years.pop()
                query = f"""
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
                                    WHERE year='{last_year}' 
                                )
                            )
                        )
                ) """
                if years:
                    for year in years:
                        query += f"""
                        INTERSECT 
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
                                        )
                                    )
                                )
                        ) """
            else:
                last_year = years.pop()
                query = f"""
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
                            WHERE year='{last_year}' 
                        )
                    )
                ) """
                if years:
                    for year in years:
                        query += f"""
                        INTERSECT 
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
                                )
                            )
                        ) """
            query += ";"
            self._cur.execute(query)
            res = self._cur.fetchall()
            if res:
                return [[x[0], x[1].replace("_", " ")] for x in res]
            return []
        except psycopg2.Error as e:
            print("???????????? ?????????????????? ???????????? ???? ???? " + str(e))
