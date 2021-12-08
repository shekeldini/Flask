from report_classes.classBaseReport import BaseReport


class ResultVpr(BaseReport):
    def __init__(self, request, dbase, user):
        super().__init__(request, dbase, user)

    def get_report(self):
        content = self._report_type["name"]
        sub_content = [f"ВПР 2021. {self._parallel['name']} класс",
                       f"Предмет: {self._subject['name']}"]
        if self._district["id"] != "all":
            if self._oo["id"] != "all":
                percents = {"all_districts": {},
                            "district": {},
                            "oo": {}}

                percents_oo = self._dbase.get_result_vpr(
                    id_oo_parallels_subjects=self._subject["id"],
                    id_oo_parallels=self._parallel["id"])

                percents_district = self._dbase.get_result_vpr_for_all_school_in_district(
                    id_user=self._user.get_id(),
                    id_district=self._district["id"],
                    id_subjects=self._dbase.get_subject_id(self._subject["name"]),
                    parallel=self._parallel["name"])

                percents_all = self._dbase.get_result_vpr_for_all_districts(
                    id_user=self._user.get_id(),
                    id_subjects=self._dbase.get_subject_id(self._subject["name"]),
                    parallel=self._parallel["name"])

                percents["oo"]["name"] = self._oo["name"]
                percents["oo"]["value"] = percents_oo
                percents["district"]["name"] = self._district["name"]
                percents["district"]["value"] = percents_district
                percents["all_districts"]["name"] = "Все муниципалитеты"
                percents["all_districts"]["value"] = percents_all

                return {"table_settings": {
                    "titles": ['Группы участников', 'Кол-во участников', '2', '3', '4', '5', "Средняя отметка",
                               "Качество обученности", "Успеваемость"],
                    "fields": ["count_of_students", '2', '3', '4', '5', "mean_mark", "quality", "performance"],
                    "values": percents,
                    "district": self._district,
                    "oo": self._oo},
                    "content": content,
                    "sub_content": sub_content}

            elif self._oo["id"] == "all":
                percents = {"all_districts": {},
                            "district": {}}
                percents["district"]["schools"] = {}

                percents_district = self._dbase.get_result_vpr_for_all_school_in_district(
                    id_user=self._user.get_id(),
                    id_district=self._district["id"],
                    id_subjects=self._subject["id"],
                    parallel=self._parallel["id"])

                for id_oo_parallels_subjects, id_oo_parallels in self._dbase.get_oo_from_id_oo_parallels_subjects(
                        id_district=self._district["id"],
                        id_user=self._user.get_id(),
                        parallel=self._parallel["id"],
                        id_subjects=self._dbase.get_subject_id(self._subject["name"])):
                    school_name = self._dbase.get_oo_name_from_oo_parallels(id_oo_parallels=id_oo_parallels)

                    school_percents = self._dbase.get_result_vpr(id_oo_parallels_subjects=id_oo_parallels_subjects,
                                                                 id_oo_parallels=id_oo_parallels)

                    percents["district"]["schools"][school_name] = school_percents

                percents_all = self._dbase.get_result_vpr_for_all_districts(
                    id_user=self._user.get_id(),
                    id_subjects=self._dbase.get_subject_id(self._subject["name"]),
                    parallel=self._parallel["name"])

                percents["district"]["name"] = self._district["name"]
                percents["district"]["value"] = percents_district
                percents["all_districts"]["name"] = "Все муниципалитеты"
                percents["all_districts"]["value"] = percents_all

                return {"table_settings": {
                    "titles": ['Группы участников', 'Кол-во участников', '2', '3', '4', '5', "Средняя отметка",
                               "Качество обученности", "Успеваемость"],
                    "fields": ["count_of_students", '2', '3', '4', '5', "mean_mark", "quality", "performance"],
                    "values": percents,
                    "district": self._district,
                    "oo": self._oo},
                    "content": content,
                    "sub_content": sub_content}

        elif self._district["id"] == "all":
            if self._oo["id"] == "all":
                percents = {"all_districts": {}}
                percents["all_districts"]["districts"] = {}

                percents_all = self._dbase.get_result_vpr_for_all_districts(
                    id_user=self._user.get_id(),
                    id_subjects=self._subject["id"],
                    parallel=self._parallel["id"])

                for id_district, district_name in self._dbase.get_district_for_report_type_2(id_user=self._user.get_id(),
                                                                                             id_subjects=self._subject[
                                                                                                 "id"],
                                                                                             parallel=self._parallel["id"]):
                    percents_district = self._dbase.get_result_vpr_for_all_school_in_district(
                        id_user=self._user.get_id(),
                        id_district=id_district,
                        id_subjects=self._subject["id"],
                        parallel=self._parallel["id"])
                    percents["all_districts"]["districts"][district_name.replace("_", " ")] = percents_district
                percents["all_districts"]["name"] = "Все муниципалитеты"
                percents["all_districts"]["value"] = percents_all

                return {"table_settings": {
                    "titles": ['Группы участников', 'Кол-во участников', '2', '3', '4', '5', "Средняя отметка",
                               "Качество обученности", "Успеваемость"],
                    "fields": ["count_of_students", '2', '3', '4', '5', "mean_mark", "quality", "performance"],
                    "values": percents,
                    "district": self._district,
                    "oo": self._oo},
                    "content": content,
                    "sub_content": sub_content}
