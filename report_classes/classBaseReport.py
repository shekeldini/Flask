class BaseReport:
    def __init__(self, request, dbase, user):
        self._years = request.get("year")
        self._district = request.get("district")
        self._oo = request.get("oo")
        self._parallel = request.get("parallel")
        self._subject = request.get("subject")
        self._report_type = request.get("report")
        self._request = request
        self._dbase = dbase
        self._user = user
        self._year = request.get("year")
