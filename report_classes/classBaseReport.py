class BaseReport:
    def __init__(self, request, dbase, user):
        self._district = request["district"]
        self._oo = request["oo"]
        self._parallel = request["parallel"]
        self._subject = request["subject"]
        self._report_type = request["report"]
        self._dbase = dbase
        self._user = user
