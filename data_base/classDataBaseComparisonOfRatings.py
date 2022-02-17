import psycopg2

from data_base.postgresql import Postgresql


class DataBaseComparisonOfRatings(Postgresql):
    def __init__(self, connection):
        super().__init__(connection)

    def get_comparison_of_ratings_for_all_districts(self, id_subjects, parallel, year):
        try:
            self._cur.execute(f"""
            SELECT result, COUNT(result) FROM
            (
                SELECT id_students,
                CASE 
                WHEN mark_for_vpr<mark_for_last_semester THEN 'понизил'
                WHEN mark_for_vpr>mark_for_last_semester THEN 'повысил'
                WHEN mark_for_vpr=mark_for_last_semester THEN 'подтвердил'
                END AS result FROM 
                (
                    SELECT id_students,sum_marks, mark_for_last_semester,
                    CASE 
                    WHEN sum_marks<mark_three THEN 2
                    WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                    WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                    WHEN sum_marks>=mark_five THEN 5
                    ELSE 0
                    END AS mark_for_vpr FROM 
                    (
                        SELECT id_students, sum_marks, mark_for_last_semester, mark_three, mark_four, mark_five FROM 
                        (
                            (
                                SELECT id_students, mark_for_last_semester, id_oo_parallels_subjects, SUM(mark) as sum_marks FROM result_for_task 
                                WHERE id_subjects={id_subjects} 
                                AND id_oo_parallels_subjects IN 
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
                                        )
                                    )
                                ) GROUP BY id_students, id_oo_parallels_subjects, mark_for_last_semester
                            ) AS t1
                            LEFT JOIN 
                            (
                                SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five FROM oo_parallels_subjects 
                                WHERE id_subjects={id_subjects} 
                                AND id_oo_parallels IN 
                                (
                                    SELECT id_oo_parallels FROM oo_parallels 
                                    WHERE parallel={parallel}
                                )
                            ) AS t2 
                            USING (id_oo_parallels_subjects)
                        )
                    ) AS t3
                ) AS t4
            ) AS t5 
            GROUP BY result;""")
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
            (
                SELECT id_students,
                CASE 
                WHEN mark_for_vpr<mark_for_last_semester THEN 'понизил'
                WHEN mark_for_vpr>mark_for_last_semester THEN 'повысил'
                WHEN mark_for_vpr=mark_for_last_semester THEN 'подтвердил'
                END AS result FROM 
                (
                    SELECT id_students,sum_marks, mark_for_last_semester,
                    CASE 
                    WHEN sum_marks<mark_three THEN 2
                    WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                    WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                    WHEN sum_marks>=mark_five THEN 5
                    ELSE 0
                    END AS mark_for_vpr FROM 
                    (
                        SELECT id_students, sum_marks, mark_for_last_semester, mark_three, mark_four, mark_five FROM 
                        (
                            (
                                SELECT id_students, mark_for_last_semester, id_oo_parallels_subjects, SUM(mark) as sum_marks FROM result_for_task 
                                WHERE id_subjects={id_subjects} 
                                AND id_oo_parallels_subjects IN 
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
                                ) GROUP BY id_students, id_oo_parallels_subjects, mark_for_last_semester
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
            ) AS t5 
            GROUP BY result;""")
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

    def get_comparison_of_ratings(self, id_oo_parallels_subjects, id_oo_parallels):
        try:
            self._cur.execute(f"""
            SELECT result, COUNT(result) FROM
            (
                SELECT id_students,
                CASE 
                WHEN mark_for_vpr<mark_for_last_semester THEN 'понизил'
                WHEN mark_for_vpr>mark_for_last_semester THEN 'повысил'
                WHEN mark_for_vpr=mark_for_last_semester THEN 'подтвердил'
                END AS result FROM 
                (
                    SELECT id_students,sum_marks, mark_for_last_semester,
                    CASE 
                    WHEN sum_marks<mark_three THEN 2
                    WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                    WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                    WHEN sum_marks>=mark_five THEN 5
                    ELSE 0
                    END AS mark_for_vpr FROM 
                    (
                        SELECT id_students, sum_marks, mark_three, mark_four, mark_five, mark_for_last_semester FROM 
                        (
                            SELECT id_students, id_oo_parallels_subjects, mark_for_last_semester, SUM(mark) as sum_marks FROM result_for_task 
                            WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects} 
                            AND id_oo_parallels = {id_oo_parallels}
                            GROUP BY id_students, id_oo_parallels_subjects, mark_for_last_semester
                        ) AS t1
                        LEFT JOIN 
                        (
                            SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five FROM oo_parallels_subjects 
                            WHERE id_oo_parallels_subjects = {id_oo_parallels_subjects}
                        ) AS t2
                        USING (id_oo_parallels_subjects)
                    ) AS t3
                ) AS t4
            ) AS t5 
            GROUP BY result;""")
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
