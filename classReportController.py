from report_classes.classStatisticsOfMarks import StatisticsOfMarks
from report_classes.classComparisonOfRatings import ComparisonOfRatings
from report_classes.classResultVpr import ResultVpr
from report_classes.classSchoolRisk import SchoolsInRisk
from report_classes.classWorkDescription import WorkDescription
from report_classes.classWorkDescriptionForOneTask import WorkDescriptionForOneTask


class ReportController:
    def __init__(self, request, dbase, user):
        self._request = request
        self._dbase = dbase
        self._user = user
        if int(self._request["report"]["id"]) == 0:
            self.report_cls = StatisticsOfMarks(self._request, self._dbase, self._user)

        elif int(self._request["report"]["id"]) == 1:
            self.report_cls = ComparisonOfRatings(self._request, self._dbase, self._user)

        elif int(self._request["report"]["id"]) == 2:
            self.report_cls = ResultVpr(self._request, self._dbase, self._user)

        elif int(self._request["report"]["id"]) == 3:
            self.report_cls = SchoolsInRisk(self._request, self._dbase, self._user)

        elif int(self._request["report"]["id"]) == 4:
            self.report_cls = WorkDescription(self._request, self._dbase, self._user)

        elif int(self._request["report"]["id"]) == 5:
            self.report_cls = WorkDescriptionForOneTask(self._request, self._dbase, self._user)

        else:
            self.report_cls = None

    def get_report(self):
        if self.report_cls:
            return self.report_cls.get_report()
        else:
            return {"something wrong"}

    def export_report(self):
        if self.report_cls:
            return self.report_cls.export_report()
        else:
            return None, None
