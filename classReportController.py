from report_classes.classStatisticsOfMarks import StatisticsOfMarks
from report_classes.classComparisonOfRatings import ComparisonOfRatings
from report_classes.classResultVpr import ResultVpr
from report_classes.classSchoolRisk import SchoolsInRisk
from report_classes.classWorkDescription import WorkDescription

class ReportController:
    def __init__(self, request, dbase, user):
        self._request = request
        self._dbase = dbase
        self._user = user

    def get_report(self):
        if int(self._request["report"]["id"]) == 0:
            report_cls = StatisticsOfMarks(self._request, self._dbase, self._user)
            return report_cls.get_report()

        elif int(self._request["report"]["id"]) == 1:
            report_cls = ComparisonOfRatings(self._request, self._dbase, self._user)
            return report_cls.get_report()

        elif int(self._request["report"]["id"]) == 2:
            report_cls = ResultVpr(self._request, self._dbase, self._user)
            return report_cls.get_report()

        elif int(self._request["report"]["id"]) == 3:
            report_cls = SchoolsInRisk(self._request, self._dbase, self._user)
            return report_cls.get_report()

        elif int(self._request["report"]["id"]) == 4:
            report_cls = WorkDescription(self._request, self._dbase, self._user)
            return report_cls.get_report()
