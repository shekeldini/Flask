from report_classes.classBaseReport import BaseReport


class SchoolsInRisk(BaseReport):
    def __init__(self, request, dbase, user):
        super().__init__(request, dbase, user)

    def get_report(self):
        if self._district["id"] != "all":
            if self._oo["id"] != "all":
                res = self._dbase.get_schools_in_risk_for_oo(id_oo_parallels_subjects=self._subject["id"],
                                                             id_oo_parallels=self._parallel["id"])
                return {"plot_settings": {"lables": [2, 3, 4, 5],
                                         "content": self._oo["name"],
                                         "sub_content": [f"ВПР 2021. {self._parallel['name']} класс",
                                                         f"Предмет: {self._subject['name']}"],
                                         "title": "Сравнение отметок с отметками по журналу",
                                         "x_axis": "Отметки",
                                         "y_axis": "Кол-во участников"},
                        "table_settings": {
                            "titles": ['Района', 'Название ОО', 'Кол-во участников', '2', '3', '4', '5', '2', '3', '4', '5'],
                            "fields": ['2', '3', '4', '5'],
                            "district": self._district["name"],
                            "oo": self._oo["name"],
                            "content": "Необъективные результаты ВПР"},
                        "values": res
                        }

