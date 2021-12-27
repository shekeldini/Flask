from report_classes.classBaseReport import BaseReport
from openpyxl import Workbook


class WorkDescriptionForOneTask(BaseReport):
    def __init__(self, request, dbase, user):
        super().__init__(request, dbase, user)
        self.task = request["task"]

    def get_report(self):
        if self._district["id"] != "all":
            if self._oo["id"] != "all":
                oo = self._dbase.get_task_description_for_one_task_for_oo(id_oo_parallels_subjects=self._subject["id"],
                                                                          task_number=self.task["id"])

                district = self._dbase.get_task_description_for_one_task_for_district(
                    id_district=self._district["id"],
                    id_subjects=self._dbase.get_subject_id(self._subject["name"]),
                    parallel=self._parallel["name"],
                    task_number=self.task["id"])

                all_ = self._dbase.get_task_description_for_one_task_for_all(
                    id_subjects=self._dbase.get_subject_id(self._subject["name"]),
                    parallel=self._parallel["name"],
                    task_number=self.task["id"])
                return {"table_settings": {"titles": ["Номер задания",
                                                      "Блоки ПООП обучающийся научится "
                                                      "/ получит возможность научиться "
                                                      "или проверяемые требования (умения) "
                                                      "в соответствии с ФГОС (ФК ГОС)", "Макс балл",
                                                      "Все муниципалитеты", self._district["name"], self._oo["name"]],
                                           "title": "Описание контрольных измерительных материалов"},
                        "values_array": {"oo": {"values": oo},
                                         "district": {"values": district},
                                         "all": {"values": all_}}}

            elif self._oo["id"] == "all":
                district = self._dbase.get_task_description_for_one_task_for_district(
                    id_district=self._district["id"],
                    id_subjects=self._dbase.get_subject_id(self._subject["name"]),
                    parallel=self._parallel["name"],
                    task_number=self.task["id"])

                all_ = self._dbase.get_task_description_for_one_task_for_all(
                    id_subjects=self._dbase.get_subject_id(self._subject["name"]),
                    parallel=self._parallel["name"],
                    task_number=self.task["id"])
                return {"table_settings": {"titles": ["Номер задания",
                                                      "Блоки ПООП обучающийся научится "
                                                      "/ получит возможность научиться "
                                                      "или проверяемые требования (умения) "
                                                      "в соответствии с ФГОС (ФК ГОС)", "Макс балл",
                                                      "Все муниципалитеты", self._district["name"]],
                                           "title": "Описание контрольных измерительных материалов"},
                        "values_array": {"district": {"values": district},
                                         "all": {"values": all_}}}

        elif self._district["id"] == "all":
            if self._oo["id"] == "all":
                all_ = self._dbase.get_task_description_for_one_task_for_all(
                    id_subjects=self._dbase.get_subject_id(self._subject["name"]),
                    parallel=self._parallel["name"],
                    task_number=self.task["id"])

                return {"table_settings": {"titles": ["Номер задания",
                                                      "Блоки ПООП обучающийся научится "
                                                      "/ получит возможность научиться "
                                                      "или проверяемые требования (умения) "
                                                      "в соответствии с ФГОС (ФК ГОС)", "Макс балл",
                                                      self._district["name"]],
                                           "title": "Описание контрольных измерительных материалов"},
                        "values_array": {"all": {"values": all_}}}

    def export_report(self):
        return {}, None
