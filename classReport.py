class Report:
    def __init__(self, request, dbase, user):
        self.__district = request["district"]
        self.__oo = request["oo"]
        self.__parallel = request["parallel"]
        self.__subject = request["subject"]
        self.__report_type = request["report"]
        self.__dbase = dbase
        self.__user = user

    def __statistics_of_marks(self):
        title = "Общая гистограмма отметок"
        x_axis = "Отметка"
        y_axis = "% участников"
        content = self.__report_type["name"]
        sub_content = [f"ВПР 2021. {self.__parallel['name']} класс",
                       f"Предмет: {self.__subject['name']}"]
        if self.__district["id"] != "all":
            if self.__oo["id"] != "all":
                percents = {"all_districts": {},
                            "district": {},
                            "oo": {}}
                count_of_all_students = {"all_districts": {},
                                         "district": {},
                                         "oo": {}}

                percents_oo, count_of_all_students_oo = self.__dbase.get_count_students_mark(
                    id_oo_parallels_subjects=self.__subject["id"],
                    id_oo_parallels=self.__parallel["id"])

                percents_district, count_of_all_students_district = self.__dbase.get_count_students_mark_for_all_school_in_district(
                    id_user=self.__user.get_id(),
                    id_district=self.__district["id"],
                    id_subjects=self.__dbase.get_subject_id(self.__subject["name"]),
                    parallel=self.__parallel["name"])

                percents_all, count_of_all_students_all = self.__dbase.get_count_students_mark_for_all_districts(
                    id_user=self.__user.get_id(),
                    id_subjects=self.__dbase.get_subject_id(self.__subject["name"]),
                    parallel=self.__parallel["name"])

                percents["oo"]["name"] = self.__oo["name"]
                percents["oo"]["value"] = percents_oo
                percents["district"]["name"] = self.__district["name"]
                percents["district"]["value"] = percents_district
                percents["all_districts"]["name"] = "Все муниципалитеты"
                percents["all_districts"]["value"] = percents_all

                count_of_all_students["oo"]["name"] = self.__oo["name"]
                count_of_all_students["oo"]["value"] = count_of_all_students_oo
                count_of_all_students["district"]["name"] = self.__district["name"]
                count_of_all_students["district"]["value"] = count_of_all_students_district
                count_of_all_students["all_districts"]["name"] = "Все муниципалитеты"
                count_of_all_students["all_districts"]["value"] = count_of_all_students_all

                return {"plot_settings": {"lables": [2, 3, 4, 5],
                                          "content": content,
                                          "sub_content": sub_content,
                                          "title": title,
                                          "x_axis": x_axis,
                                          "y_axis": y_axis},
                        "table_settings": {"titles": ['Группы участников', 'Кол-во участников', '2', '3', '4', '5'],
                                           "fields": ['groups', 'count_of_all_students', '2', '3', '4', '5'],
                                           "values": {'groups': [percents[x]["name"] for x in percents],
                                                      "count_of_all_students": [count_of_all_students[x]["value"] for x
                                                                                in count_of_all_students],
                                                      "2": [percents[x]["value"][2] for x in percents],
                                                      "3": [percents[x]["value"][3] for x in percents],
                                                      "4": [percents[x]["value"][4] for x in percents],
                                                      "5": [percents[x]["value"][5] for x in percents]}},
                        "district": self.__district,
                        "oo": self.__oo,
                        "percents": percents,
                        }

            elif self.__oo["id"] == "all":
                percents = {"all_districts": {},
                            "district": {}}
                count_of_all_students = {"all_districts": {},
                                         "district": {}}
                percents_district, count_of_all_students_district = self.__dbase.get_count_students_mark_for_all_school_in_district(
                    id_user=self.__user.get_id(),
                    id_district=self.__district["id"],
                    id_subjects=self.__subject["id"],
                    parallel=self.__parallel["id"])

                percents_all, count_of_all_students_all = self.__dbase.get_count_students_mark_for_all_districts(
                    id_user=self.__user.get_id(),
                    id_subjects=self.__dbase.get_subject_id(self.__subject["name"]),
                    parallel=self.__parallel["name"])

                percents["district"]["name"] = self.__district["name"]
                percents["district"]["value"] = percents_district
                percents["all_districts"]["name"] = "Все муниципалитеты"
                percents["all_districts"]["value"] = percents_all

                count_of_all_students["district"]["name"] = self.__district["name"]
                count_of_all_students["district"]["value"] = count_of_all_students_district
                count_of_all_students["all_districts"]["name"] = "Все муниципалитеты"
                count_of_all_students["all_districts"]["value"] = count_of_all_students_all

                return {"plot_settings": {"lables": [2, 3, 4, 5],
                                          "content": content,
                                          "sub_content": sub_content,
                                          "title": title,
                                          "x_axis": x_axis,
                                          "y_axis": y_axis},
                        "table_settings": {"titles": ['Группы участников', 'Кол-во участников', '2', '3', '4', '5'],
                                           "fields": ['groups', 'count_of_all_students', '2', '3', '4', '5'],
                                           "values": {'groups': [percents[x]["name"] for x in percents],
                                                      "count_of_all_students": [count_of_all_students[x]["value"] for x
                                                                                in count_of_all_students],
                                                      "2": [percents[x]["value"][2] for x in percents],
                                                      "3": [percents[x]["value"][3] for x in percents],
                                                      "4": [percents[x]["value"][4] for x in percents],
                                                      "5": [percents[x]["value"][5] for x in percents]}},
                        "district": self.__district,
                        "oo": self.__oo,
                        "percents": percents,
                        }

        elif self.__district["id"] == "all":
            if self.__oo["id"] == "all":
                percents = {"all_districts": {}}
                count_of_all_students = {"all_districts": {}}

                percents_all, count_of_all_students_all = self.__dbase.get_count_students_mark_for_all_districts(
                    id_user=self.__user.get_id(),
                    id_subjects=self.__subject["id"],
                    parallel=self.__parallel["id"])

                percents["all_districts"]["name"] = "Все муниципалитеты"
                percents["all_districts"]["value"] = percents_all

                count_of_all_students["all_districts"]["name"] = "Все муниципалитеты"
                count_of_all_students["all_districts"]["value"] = count_of_all_students_all

                return {"plot_settings": {"lables": [2, 3, 4, 5],
                                          "content": content,
                                          "sub_content": sub_content,
                                          "title": title,
                                          "x_axis": x_axis,
                                          "y_axis": y_axis},
                        "table_settings": {"titles": ['Группы участников', 'Кол-во участников', '2', '3', '4', '5'],
                                           "fields": ['groups', 'count_of_all_students', '2', '3', '4', '5'],
                                           "values": {'groups': [percents[x]["name"] for x in percents],
                                                      "count_of_all_students": [count_of_all_students[x]["value"] for x
                                                                                in count_of_all_students],
                                                      "2": [percents[x]["value"][2] for x in percents],
                                                      "3": [percents[x]["value"][3] for x in percents],
                                                      "4": [percents[x]["value"][4] for x in percents],
                                                      "5": [percents[x]["value"][5] for x in percents]}},
                        "district": self.__district,
                        "oo": self.__oo,
                        "percents": percents,
                        }

    def __comparison_of_ratings(self):
        title = "Гистограмма соотвествия отметок за выполненную работу и отметок по журналу"
        x_axis = ""
        y_axis = "Количество участников в %"
        content = self.__report_type["name"]

        if self.__district["id"] != "all":
            if self.__oo["id"] != "all":
                sub_content = {"all_districts": [f"Все муниципалитеты",
                                                 f"ВПР 2021. {self.__parallel['name']} класс",
                                                 f"Предмет: {self.__subject['name']}"],
                               "district": [f"{self.__district['name']}",
                                            f"ВПР 2021. {self.__parallel['name']} класс",
                                            f"Предмет: {self.__subject['name']}"],
                               "oo": [f"{self.__oo['name']}",
                                      f"ВПР 2021. {self.__parallel['name']} класс",
                                      f"Предмет: {self.__subject['name']}"],
                               "all": [f"Сравнительный анализ",
                                       f"ВПР 2021. {self.__parallel['name']} класс",
                                       f"Предмет: {self.__subject['name']}"
                                       ]}

                percents = {"all_districts": {},
                            "district": {},
                            "oo": {}}

                percents_oo = self.__dbase.get_comparison_of_ratings(
                    id_oo_parallels_subjects=self.__subject["id"],
                    id_oo_parallels=self.__parallel["id"])

                percents_district = self.__dbase.get_comparison_of_ratings_for_all_schools_in_district(
                    id_user=self.__user.get_id(),
                    id_district=self.__district["id"],
                    id_subjects=self.__dbase.get_subject_id(self.__subject["name"]),
                    parallel=self.__parallel["name"])

                percents_all = self.__dbase.get_comparison_of_ratings_for_all_districts(
                    id_user=self.__user.get_id(),
                    id_subjects=self.__dbase.get_subject_id(self.__subject["name"]),
                    parallel=self.__parallel["name"])

                percents["oo"]["name"] = self.__oo["name"]
                percents["oo"]["value"] = percents_oo
                percents["district"]["name"] = self.__district["name"]
                percents["district"]["value"] = percents_district
                percents["all_districts"]["name"] = "Все муниципалитеты"
                percents["all_districts"]["value"] = percents_all

                return {"plot_settings": {"lables": ['Понизили', 'Подтвердили', 'Повысили'],
                                          "content": content,
                                          "sub_content": sub_content,
                                          "title": title,
                                          "x_axis": x_axis,
                                          "y_axis": y_axis},
                        "table_settings": {"titles": ['Группы участников', 'Кол-во участников', '%'],
                                           "fields": ['groups', 'count_of_all_students', '%'],
                                           'groups': ['Понизили (Отметка < Отметка по журналу)',
                                                      'Подтвердили (Отметка = Отметка по журналу)',
                                                      "Повысили (Отметка > Отметка по журналу)",
                                                      "Всего"]},
                        "district": self.__district,
                        "oo": self.__oo,
                        "percents": percents,
                        }

            elif self.__oo["id"] == "all":
                sub_content = {"all_districts": [f"Все муниципалитеты",
                                                 f"ВПР 2021. {self.__parallel['name']} класс",
                                                 f"Предмет: {self.__subject['name']}"],
                               "district": [f"{self.__district['name']}",
                                            f"ВПР 2021. {self.__parallel['name']} класс",
                                            f"Предмет: {self.__subject['name']}"]}
                percents = {"all_districts": {},
                            "district": {}}

                percents_district = self.__dbase.get_comparison_of_ratings_for_all_schools_in_district(
                    id_user=self.__user.get_id(),
                    id_district=self.__district["id"],
                    id_subjects=self.__dbase.get_subject_id(self.__subject["name"]),
                    parallel=self.__parallel["name"])

                percents_all = self.__dbase.get_comparison_of_ratings_for_all_districts(
                    id_user=self.__user.get_id(),
                    id_subjects=self.__dbase.get_subject_id(self.__subject["name"]),
                    parallel=self.__parallel["name"])

                percents["district"]["name"] = self.__district["name"]
                percents["district"]["value"] = percents_district
                percents["all_districts"]["name"] = "Все муниципалитеты"
                percents["all_districts"]["value"] = percents_all

                return {"plot_settings": {"lables": ['Понизили', 'Подтвердили', 'Повысили'],
                                          "content": content,
                                          "sub_content": sub_content,
                                          "title": title,
                                          "x_axis": x_axis,
                                          "y_axis": y_axis},
                        "table_settings": {"titles": ['Группы участников', 'Кол-во участников', '%'],
                                           'groups': ['Понизили (Отметка < Отметка по журналу)',
                                                      'Подтвердили (Отметка = Отметка по журналу)',
                                                      "Повысили (Отметка > Отметка по журналу)",
                                                      "Всего"]},
                        "district": self.__district,
                        "oo": self.__oo,
                        "percents": percents,
                        }

        elif self.__district["id"] == "all":
            sub_content = {"all_districts": [f"Все муниципалитеты",
                                             f"ВПР 2021. {self.__parallel['name']} класс",
                                             f"Предмет: {self.__subject['name']}"]}
            if self.__oo["id"] == "all":
                percents = {"all_districts": {}}
                percents_all = self.__dbase.get_comparison_of_ratings_for_all_districts(
                    id_user=self.__user.get_id(),
                    id_subjects=self.__dbase.get_subject_id(self.__subject["name"]),
                    parallel=self.__parallel["name"])

                percents["all_districts"]["name"] = "Все муниципалитеты"
                percents["all_districts"]["value"] = percents_all

                return {"plot_settings": {"lables": ['Понизили', 'Подтвердили', 'Повысили'],
                                          "content": content,
                                          "sub_content": sub_content,
                                          "title": title,
                                          "x_axis": x_axis,
                                          "y_axis": y_axis},
                        "table_settings": {"titles": ['Группы участников', 'Кол-во участников', '%'],
                                           'groups': ['Понизили (Отметка < Отметка по журналу)',
                                                      'Подтвердили (Отметка = Отметка по журналу)',
                                                      "Повысили (Отметка > Отметка по журналу)",
                                                      "Всего"]},
                        "district": self.__district,
                        "oo": self.__oo,
                        "percents": percents,
                        }

    def __result_vpr(self):
        content = self.__report_type["name"]
        sub_content = [f"ВПР 2021. {self.__parallel['name']} класс",
                       f"Предмет: {self.__subject['name']}"]
        if self.__district["id"] != "all":
            if self.__oo["id"] != "all":
                percents = {"all_districts": {},
                            "district": {},
                            "oo": {}}

                percents_oo = self.__dbase.get_result_vpr(
                    id_oo_parallels_subjects=self.__subject["id"],
                    id_oo_parallels=self.__parallel["id"])

                percents_district = self.__dbase.get_result_vpr_for_all_school_in_district(
                    id_user=self.__user.get_id(),
                    id_district=self.__district["id"],
                    id_subjects=self.__dbase.get_subject_id(self.__subject["name"]),
                    parallel=self.__parallel["name"])

                percents_all = self.__dbase.get_result_vpr_for_all_districts(
                    id_user=self.__user.get_id(),
                    id_subjects=self.__dbase.get_subject_id(self.__subject["name"]),
                    parallel=self.__parallel["name"])

                percents["oo"]["name"] = self.__oo["name"]
                percents["oo"]["value"] = percents_oo
                percents["district"]["name"] = self.__district["name"]
                percents["district"]["value"] = percents_district
                percents["all_districts"]["name"] = "Все муниципалитеты"
                percents["all_districts"]["value"] = percents_all

                return {"table_settings": {
                    "titles": ['Группы участников', 'Кол-во участников', '2', '3', '4', '5', "Средняя отметка",
                               "Качество обученности", "Успеваемость"],
                    "fields": ["count_of_students", '2', '3', '4', '5', "mean_mark", "quality", "performance"],
                    "values": percents,
                    "district": self.__district,
                    "oo": self.__oo},
                    "content": content,
                    "sub_content": sub_content}

            elif self.__oo["id"] == "all":
                percents = {"all_districts": {},
                            "district": {}}
                percents["district"]["schools"] = {}

                percents_district = self.__dbase.get_result_vpr_for_all_school_in_district(
                    id_user=self.__user.get_id(),
                    id_district=self.__district["id"],
                    id_subjects=self.__subject["id"],
                    parallel=self.__parallel["id"])

                for id_oo_parallels_subjects, id_oo_parallels in self.__dbase.get_oo_from_id_oo_parallels_subjects(
                        id_district=self.__district["id"],
                        id_user=self.__user.get_id(),
                        parallel=self.__parallel["id"],
                        id_subjects=self.__dbase.get_subject_id(self.__subject["name"])):
                    school_name = self.__dbase.get_oo_name_from_oo_parallels(id_oo_parallels=id_oo_parallels)

                    school_percents = self.__dbase.get_result_vpr(id_oo_parallels_subjects=id_oo_parallels_subjects,
                                                                  id_oo_parallels=id_oo_parallels)

                    percents["district"]["schools"][school_name] = school_percents

                percents_all = self.__dbase.get_result_vpr_for_all_districts(
                    id_user=self.__user.get_id(),
                    id_subjects=self.__dbase.get_subject_id(self.__subject["name"]),
                    parallel=self.__parallel["name"])

                percents["district"]["name"] = self.__district["name"]
                percents["district"]["value"] = percents_district
                percents["all_districts"]["name"] = "Все муниципалитеты"
                percents["all_districts"]["value"] = percents_all

                return {"table_settings": {
                    "titles": ['Группы участников', 'Кол-во участников', '2', '3', '4', '5', "Средняя отметка",
                               "Качество обученности", "Успеваемость"],
                    "fields": ["count_of_students", '2', '3', '4', '5', "mean_mark", "quality", "performance"],
                    "values": percents,
                    "district": self.__district,
                    "oo": self.__oo},
                    "content": content,
                    "sub_content": sub_content}

        elif self.__district["id"] == "all":
            if self.__oo["id"] == "all":
                percents = {"all_districts": {}}
                percents["all_districts"]["districts"] = {}

                percents_all = self.__dbase.get_result_vpr_for_all_districts(
                    id_user=self.__user.get_id(),
                    id_subjects=self.__subject["id"],
                    parallel=self.__parallel["id"])

                for id_district, district_name in self.__dbase.get_district_for_report_type_2(id_user=self.__user.get_id(),
                                                                                              id_subjects=self.__subject["id"],
                                                                                              parallel=self.__parallel["id"]):
                    percents_district = self.__dbase.get_result_vpr_for_all_school_in_district(
                        id_user=self.__user.get_id(),
                        id_district=id_district,
                        id_subjects=self.__subject["id"],
                        parallel=self.__parallel["id"])
                    percents["all_districts"]["districts"][district_name.replace("_", " ")] = percents_district

                percents["all_districts"]["name"] = "Все муниципалитеты"
                percents["all_districts"]["value"] = percents_all

                return {"table_settings": {
                    "titles": ['Группы участников', 'Кол-во участников', '2', '3', '4', '5', "Средняя отметка",
                               "Качество обученности", "Успеваемость"],
                    "fields": ["count_of_students", '2', '3', '4', '5', "mean_mark", "quality", "performance"],
                    "values": percents,
                    "district": self.__district,
                    "oo": self.__oo},
                    "content": content,
                    "sub_content": sub_content}

    def get_report(self):
        if int(self.__report_type["id"]) == 0:
            return self.__statistics_of_marks()

        elif int(self.__report_type["id"]) == 1:
            return self.__comparison_of_ratings()

        elif int(self.__report_type["id"]) == 2:
            return self.__result_vpr()

