import psycopg2
from configurations.development import Config
from data_base.postgresql import Postgresql


class TasksByGroups(Postgresql):
    def __init__(self, connection):
        super().__init__(connection)

    def get_tasks_by_groups_for_all(self, id_subjects: int, parallel: int, year: str) -> dict:
        result = {}
        for mark in range(2, 6):
            query = f"""
            SELECT task_number, task_number_from_kim, max_mark, complete, count(complete) FROM
            (
                SELECT id_students, task_number, task_number_from_kim, max_mark, 
                CASE
                WHEN mark = max_mark THEN 'complete'
                WHEN mark != max_mark THEN 'not complete'
                END AS complete FROM
                (
                    SELECT id_students, task_number, task_number_from_kim, mark, max_mark FROM
                    (
                        (
                            SELECT id_students, task_number, mark, id_distributio_of_tasks_by_positions_of_codifiers FROM result_for_task
                            WHERE id_oo_parallels_subjects IN
                            (
                                SELECT id_oo_parallels_subjects FROM oo_parallels_subjects
                                WHERE id_oo_parallels IN
                                (
                                    SELECT id_oo_parallels FROM oo_parallels
                                    WHERE parallel = {parallel}
                                    AND id_oo in
                                    (
                                        SELECT id_oo FROM oo
                                        WHERE year = '{year}'
                                    )
                                )
                                AND id_subjects = {id_subjects}
                            )
                            AND id_students IN
                            (
                                SELECT id_students FROM
                                (
                                    SELECT id_students,sum_marks,
                                    CASE
                                    WHEN sum_marks<mark_three THEN 2
                                    WHEN sum_marks>=mark_three AND sum_marks<mark_four THEN 3
                                    WHEN sum_marks>=mark_four AND sum_marks<mark_five THEN 4
                                    WHEN sum_marks>=mark_five THEN 5
                                    ELSE 0
                                    END AS mark FROM
                                    (
                                        SELECT id_students, sum_marks, mark_three, mark_four, mark_five FROM
                                        (
                                            (
                                                SELECT id_students, id_oo_parallels_subjects, SUM(mark) as sum_marks FROM result_for_task
                                                WHERE id_subjects = {id_subjects}
                                                AND id_oo_parallels_subjects IN
                                                (
                                                    SELECT id_oo_parallels_subjects FROM oo_parallels_subjects
                                                    WHERE id_oo_parallels IN
                                                    (
                                                        SELECT id_oo_parallels FROM oo_parallels
                                                        WHERE parallel = {parallel}
                                                        AND id_oo in
                                                        (
                                                            SELECT id_oo FROM oo
                                                            WHERE year = '{year}'
                                                        )
                                                    )
                                                ) GROUP BY id_students, id_oo_parallels_subjects
                                            ) AS t1
            
                                            LEFT JOIN
                                            (
                                                SELECT id_oo_parallels_subjects, mark_three, mark_four, mark_five FROM oo_parallels_subjects
                                                WHERE id_subjects = {id_subjects}
                                                AND id_oo_parallels IN
                                                (
                                                    SELECT id_oo_parallels FROM oo_parallels
                                                    WHERE parallel = {parallel}
                                                    AND id_oo in
                                                    (
                                                        SELECT id_oo FROM oo
                                                        WHERE year = '{year}'
                                                    )
                                                )
                                            ) AS t2
                                            USING (id_oo_parallels_subjects)
                                        )
                                    ) AS t3
                                ) AS t4
                                WHERE mark = {mark}
                            )
                        ) AS T1
                        LEFT JOIN
                        (
                            SELECT id_distributio_of_tasks_by_positions_of_codifiers, task_number, task_number_from_kim, max_mark FROM distributio_of_tasks_by_positions_of_codifiers
                            WHERE id_subjects = {id_subjects}
                            AND parallel = {parallel}
                            AND year = '{year}'
                        ) AS T2
                        USING (id_distributio_of_tasks_by_positions_of_codifiers, task_number)
                    )
                ) AS T3
            ) AS T_R
            GROUP BY (task_number, task_number_from_kim, max_mark, complete) ORDER BY (task_number);"""
            self._cur.execute(query)
            res = self._cur.fetchall()
            if res:
                result[f"group_{mark}"] = {}
                for row in res:
                    task_number, task_number_from_kim, max_mark, complete, count = row
                    if task_number not in result[f"group_{mark}"]:
                        result[f"group_{mark}"][task_number] = {
                            "task_number_from_kim": task_number_from_kim,
                            "max_mark": max_mark,
                            "complete": {
                                "count": 0,
                                "percent": 0.
                            },
                            "not complete": {
                                "count": 0,
                                "percent": 0.
                            }
                        }
                    if complete == "complete":
                        result[f"group_{mark}"][task_number]["complete"]["count"] = count

                    elif complete == "not complete":
                        result[f"group_{mark}"][task_number]["not complete"]["count"] = count

                    count_all = result[f"group_{mark}"][task_number]["complete"]["count"] + \
                                result[f"group_{mark}"][task_number]["not complete"]["count"]

                    complete_percent = round((result[f"group_{mark}"][task_number]["complete"]["count"] / count_all) * 100, 2)
                    result[f"group_{mark}"][task_number]["complete"]["percent"] = complete_percent

                    not_complete_percent = round((result[f"group_{mark}"][task_number]["not complete"]["count"] / count_all) * 100, 2)
                    result[f"group_{mark}"][task_number]["not complete"]["percent"] = not_complete_percent

        return result


