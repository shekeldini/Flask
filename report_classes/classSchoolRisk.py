from report_classes.classBaseReport import BaseReport
from openpyxl import Workbook
import datetime

class SchoolsInRisk(BaseReport):
    def __init__(self, request, dbase, user):
        super().__init__(request, dbase, user)

    def get_report(self):
        schools = {4: {'Математика': ['sch220150', 'sch220175', 'sch220198', 'sch223197', 'sch223610', 'sch223615',
                                      'sch223763', 'sch223953', 'sch224143', 'sch224188', 'sch224199', 'sch224208',
                                      'sch224234', 'sch224235', 'sch224246', 'sch224259', 'sch224263', 'sch224268',
                                      'sch224313', 'sch224332', 'sch224353', 'sch224361', 'sch224395', 'sch226062',
                                      'sch226065'],
                       'Русский язык': ['sch220161', 'sch220175', 'sch220198', 'sch223197', 'sch223615', 'sch223646',
                                        'sch223687', 'sch223763', 'sch223953', 'sch224143', 'sch224188', 'sch224205',
                                        'sch224208', 'sch224234', 'sch224238', 'sch224246', 'sch224259', 'sch224263',
                                        'sch224268', 'sch224286', 'sch224313', 'sch224332', 'sch224353', 'sch224361',
                                        'sch224362', 'sch224397', 'sch226062', 'sch226065']},
                   5: {'Математика': ['sch220128', 'sch220163', 'sch220175', 'sch223197', 'sch223610', 'sch223953',
                                      'sch224188', 'sch224208', 'sch224246', 'sch224263', 'sch224268', 'sch224286',
                                      'sch224332', 'sch224353', 'sch224361', 'sch226059', 'sch226062', 'sch226065'],
                       'Русский язык': ['sch220128', 'sch220150', 'sch220161', 'sch220163', 'sch220175', 'sch223197',
                                        'sch223615', 'sch224208', 'sch224246', 'sch224263', 'sch224286', 'sch224313',
                                        'sch224332', 'sch224353', 'sch224361', 'sch226059', 'sch226062', 'sch226065']}}

        if self._district['id'] != 'all':
            if self._oo['id'] != 'all':
                res = self._dbase.get_schools_in_risk_for_oo(id_oo_parallels_subjects=self._subject['id'],
                                                             id_oo_parallels=self._parallel['id'])
                return {"type": "oo",
                        'plot_settings': {'lables': [2, 3, 4, 5],
                                         'content': res['school_name'],
                                         'sub_content': [f"ВПР 2021. {self._parallel['name']} класс",
                                                         f"Предмет: {self._subject['name']}"],
                                         'title': 'Сравнение отметок с отметками по журналу',
                                         'x_axis': 'Отметки',
                                         'y_axis': 'Кол-во участников'},
                        'table_settings': {
                            'titles': ['Район', 'Название ОО', 'Кол-во участников', '2', '3', '4', '5', '2', '3', '4',
                                       '5'],
                            'fields': ['2', '3', '4', '5'],
                            'content': 'Необъективные результаты ВПР'},
                        'values': res
                        }

            elif self._oo['id'] == 'all':
                res = self._dbase.get_schools_in_risk_for_district(id_district=self._district['id'],
                                                                   parallel=self._parallel['id'],
                                                                   schools=str(set(schools[int(self._parallel['id'])][
                                                                                   self._subject['name']])).replace("'", ""))
                return {"type": "district",
                        'table_settings': {
                            'titles': ['Район', 'Название ОО'],
                            'content': 'Необъективные результаты ВПР'},
                        'values': res}

        elif self._district['id'] == "all":
            res = self._dbase.get_schools_in_risk_for_all(parallel=self._parallel['id'],
                                                          schools=str(set(schools[int(self._parallel['id'])][
                                                                              self._subject['name']])).replace("'", ""))
            return {"type": "district",
                    'table_settings': {
                        'titles': ['Район', 'Название ОО'],
                        'content': 'Необъективные результаты ВПР'},
                    'values': res}

    def export_report(self):
        report = self.get_report()
        file_name = 'Shools In Risk.xlsx'
        wb = Workbook()
        ws = wb.active
        if report["type"] in ("district", "all"):

            for index, title in enumerate(report["table_settings"]["titles"]):
                ws.cell(row=1, column=index + 1, value=title)
            row_count = 2
            for key, school_list in report["values"].items():
                for school in school_list:
                    ws.cell(row=row_count, column=1, value=key)
                    ws.cell(row=row_count, column=2, value=school)
                    row_count += 1
        elif report["type"] == "oo":
            titles = report["table_settings"]["titles"]
            for index in range(3):
                ws.cell(row=1, column=index + 1, value=titles[index])
                ws.merge_cells(start_row=1, start_column=index + 1, end_row=2, end_column=index + 1)

            ws.cell(row=1, column=4, value="Отметка по школе")
            ws.merge_cells(start_row=1, start_column=4, end_row=1, end_column=7)

            ws.cell(row=1, column=8, value="Отметка по ВПР")
            ws.merge_cells(start_row=1, start_column=8, end_row=1, end_column=11)

            for index in range(3, 11):
                ws.cell(row=2, column=4 + index - 3, value=titles[index])

            ws.cell(row=3, column=1, value=report["values"]["district_name"])
            ws.cell(row=3, column=2, value=report["values"]["school_name"])
            ws.cell(row=3, column=3, value=report["values"]["count_of_students"])
            for index, value in enumerate(list(report["values"]["last_semester_results"].values())):
                ws.cell(row=3, column=4 + index, value=value)

            for index, value in enumerate(report["values"]["vpr_results"].values()):
                ws.cell(row=3, column=8 + index, value=value)

        return wb, file_name
