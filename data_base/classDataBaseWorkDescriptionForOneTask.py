import psycopg2

from data_base.postgresql import Postgresql


class DataBaseWorkDescriptionForOneTask(Postgresql):
    def __init__(self, connection):
        super().__init__(connection)

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
