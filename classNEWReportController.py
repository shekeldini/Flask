from report_classes.new.classStatisticsOfMarks import StatisticsOfMarks

from data_base.classDataBaseStatisticsOfMarks import DataBaseStatisticsOfMarks


class NEWReportController:
    def __init__(self, request, connection, user):
        self._request = request

        self._user = user
        if int(self._request["report"]["id"]) == 0:
            self._dbase = DataBaseStatisticsOfMarks(connection)
            self.report_cls = StatisticsOfMarks(self._request, self._dbase, self._user)

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
