from report_classes.classBaseReport import BaseReport


class MeanMark(BaseReport):
    def __init__(self, request, dbase, user):
        super().__init__(request, dbase, user)

    def get_report(self):
        res = {
            "status": 200,
            "name": self._district["name"],
            "text": "Средняя отметка по ВПР: "
        }
        value = self._dbase.get_mean_mark_for_district(
            id_district=self._dbase.get_id_district_by_name(self._district["name"]),
            id_subjects=self._subject["id"],
            parallel=self._parallel["id"],
            year=self._years["id"]
        )
        res['value'] = value if value else "Не участвовал"
        res['color'] = self._choice_color(value)

        return res

    @staticmethod
    def _choice_color(value: float) -> str:
        if value:
            if value >= 4.5:
                color = "#49006a"
            elif 3.5 <= value < 4.5:
                color = "#ae017e"
            elif 2.5 <= value < 3.4:
                color = "#f768a1"
            else:
                color = "#fcc5c0"
        else:
            color = 'white'
        return color
