from enum import Enum

from report_classes.classMeanMark import MeanMark
from report_classes.classStatisticsOfMarks import StatisticsOfMarks
from report_classes.classComparisonOfRatings import ComparisonOfRatings
from report_classes.classResultVpr import ResultVpr
from report_classes.classSchoolRisk import SchoolsInRisk
from report_classes.classWorkDescription import WorkDescription
from report_classes.classWorkDescriptionForOneTask import WorkDescriptionForOneTask
from data_base.classDataBaseStatisticsOfMarks import DataBaseStatisticsOfMarks
from data_base.classDataBaseComparisonOfRatings import DataBaseComparisonOfRatings
from data_base.classDataBaseResultVpr import DataBaseResultVpr
from data_base.classDataBaseSchoolsInRisk import DataBaseSchoolsInRisk
from data_base.classDataBaseWorkDescription import DataBaseWorkDescription
from data_base.classDataBaseWorkDescriptionForOneTask import DataBaseWorkDescriptionForOneTask
from data_base.map import Map


class ReportType(Enum):
    StatisticsOfMarks = 0
    ComparisonOfRatings = 1
    ResultVpr = 2
    SchoolsInRisk = 3
    WorkDescription = 4
    WorkDescriptionForOneTask = 5
    MeanMark = 6


class ReportController:
    def __init__(self, request, connection, user):
        self._request = request
        self._user = user

        if int(self._request["report"]["id"]) == ReportType.StatisticsOfMarks.value:
            self._dbase = DataBaseStatisticsOfMarks(connection)
            self.report_cls = StatisticsOfMarks(self._request, self._dbase, self._user)

        elif int(self._request["report"]["id"]) == ReportType.ComparisonOfRatings.value:
            self._dbase = DataBaseComparisonOfRatings(connection)
            self.report_cls = ComparisonOfRatings(self._request, self._dbase, self._user)

        elif int(self._request["report"]["id"]) == ReportType.ResultVpr.value:
            self._dbase = DataBaseResultVpr(connection)
            self.report_cls = ResultVpr(self._request, self._dbase, self._user)

        elif int(self._request["report"]["id"]) == ReportType.SchoolsInRisk.value:
            self._dbase = DataBaseSchoolsInRisk(connection)
            self.report_cls = SchoolsInRisk(self._request, self._dbase, self._user)

        elif int(self._request["report"]["id"]) == ReportType.WorkDescription.value:
            self._dbase = DataBaseWorkDescription(connection)
            self.report_cls = WorkDescription(self._request, self._dbase, self._user)

        elif int(self._request["report"]["id"]) == ReportType.WorkDescriptionForOneTask.value:
            self._dbase = DataBaseWorkDescriptionForOneTask(connection)
            self.report_cls = WorkDescriptionForOneTask(self._request, self._dbase, self._user)

        elif int(self._request["report"]["id"]) == ReportType.MeanMark.value:
            self._dbase = Map(connection)
            self.report_cls = MeanMark(self._request, self._dbase, self._user)

        else:
            self.report_cls = None

    def get_report(self):
        if self.report_cls:
            return self.report_cls.get_report()
        else:
            return {"status": 500}

    def export_report(self):
        if self.report_cls:
            return self.report_cls.export_report()
        else:
            return None, None
