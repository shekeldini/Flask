from report_classes.classBaseReport import BaseReport


class WorkDescription(BaseReport):
    def __init__(self, request, dbase, user):
        super().__init__(request, dbase, user)

    def get_report(self):
        if self._district["id"] != "all":
            if self._oo["id"] != "all":
                oo = self._dbase.get_task_description_for_oo(id_oo_parallels_subjects=self._subject["id"])

                district = self._dbase.get_task_description_for_district(id_district=self._district["id"],
                                                                         id_subjects=self._dbase.get_subject_id(self._subject["name"]),
                                                                         parallel=self._parallel["name"])

                all_ = self._dbase.get_task_description_for_all(id_subjects=self._dbase.get_subject_id(self._subject["name"]),
                                                                parallel=self._parallel["name"])
                return {"table_settings": {"titles": ["Номер задания",
                                                      "Блоки ПООП обучающийся научится "
                                                      "/ получит возможность научиться "
                                                      "или проверяемые требования (умения) "
                                                      "в соответствии с ФГОС (ФК ГОС)", "Макс балл",
                                                      "Все муниципалтеты", self._district["name"], self._oo["name"]]},
                        "values_array": {"oo": {"values": oo},
                                         "district": {"values": district},
                                         "all": {"values": all_}}}

            elif self._oo["id"] == "all":
                district = self._dbase.get_task_description_for_district(id_district=self._district["id"],
                                                                         id_subjects=self._subject["id"],
                                                                         parallel=self._parallel["id"])

                all_ = self._dbase.get_task_description_for_all(id_subjects=self._subject["id"],
                                                                parallel=self._parallel["id"])
                return {"table_settings": {"titles": ["Номер задания",
                                                      "Блоки ПООП обучающийся научится "
                                                      "/ получит возможность научиться "
                                                      "или проверяемые требования (умения) "
                                                      "в соответствии с ФГОС (ФК ГОС)", "Макс балл",
                                                      "Все муниципалтеты", self._district["name"]]},
                        "values_array": {"district": {"values": district},
                                         "all": {"values": all_}}}

        elif self._district["id"] == "all":
            if self._oo["id"] == "all":
                all_ = self._dbase.get_task_description_for_all(id_subjects=self._subject["id"],
                                                                parallel=self._parallel["id"])

                return {"table_settings": {"titles": ["Номер задания",
                                                      "Блоки ПООП обучающийся научится "
                                                      "/ получит возможность научиться "
                                                      "или проверяемые требования (умения) "
                                                      "в соответствии с ФГОС (ФК ГОС)", "Макс балл",
                                                      self._district["name"]]},
                        "values_array": {"all": {"values": all_}}}
