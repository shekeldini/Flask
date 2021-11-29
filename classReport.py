class Report:
    def __init__(self, request, dbase, user):
        self.__district = request["district"]
        self.__oo = request["oo"]
        self.__parallel = request["parallel"]
        self.__subject = request["subject"]
        self.__report_type = int(request["report"]["id"])
        self.__dbase = dbase
        self.__user = user

    def __statistics_of_marks(self):
        if self.__district["id"] != "all":
            if self.__oo["id"] != "all":
                percents, count_of_students = self.__dbase.get_count_students_mark(
                    id_oo_parallels_subjects=self.__subject["id"],
                    id_oo_parallels=self.__parallel["id"])

                return {"name_of_the_settlement": self.__district,
                        "oo": self.__oo,
                        "percents": percents,
                        "count_of_all_students": count_of_students}

            elif self.__oo["id"] == "all":
                percents, count_of_students = self.__dbase.get_count_students_mark_for_all_school_in_district(
                    id_user=self.__user.get_id(),
                    id_district=self.__district["id"],
                    id_subjects=self.__subject["id"],
                    parallel=self.__parallel["id"])

                return {"name_of_the_settlement": self.__district,
                        "oo": self.__oo,
                        "percents": percents,
                        "count_of_all_students": count_of_students}

        elif self.__district["id"] == "all":
            if self.__oo["id"] == "all":
                percents, count_of_students = self.__dbase.get_count_students_mark_for_all_districts(
                    id_user=self.__user.get_id(),
                    id_subjects=self.__subject["id"],
                    parallel=self.__parallel["id"])

                return {"name_of_the_settlement": self.__district,
                        "oo": self.__oo,
                        "percents": percents,
                        "count_of_all_students": count_of_students}

    def __comparison_of_ratings(self):
        if self.__district["id"] != "all":
            if self.__oo["id"] != "all":
                percents, count_of_students = self.__dbase.get_comparison_of_ratings(
                    id_oo_parallels_subjects=self.__subject["id"],
                    id_oo_parallels=self.__parallel["id"])

                return {"name_of_the_settlement": self.__district,
                        "oo": self.__oo,
                        "percents": percents,
                        "count_of_all_students": count_of_students}

            elif self.__oo["id"] == "all":
                percents, count_of_students = self.__dbase.get_comparison_of_ratings_for_all_schools_in_district(
                    id_user=self.__user.get_id(),
                    id_district=self.__district["id"],
                    id_subjects=self.__subject["id"],
                    parallel=self.__parallel["id"])

                return {"name_of_the_settlement": self.__district,
                        "oo": self.__oo,
                        "percents": percents,
                        "count_of_all_students": count_of_students}

        elif self.__district["id"] == "all":
            if self.__oo["id"] == "all":
                percents, count_of_students = self.__dbase.get_comparison_of_ratings_for_all_districts(
                    id_user=self.__user.get_id(),
                    id_subjects=self.__subject["id"],
                    parallel=self.__parallel["id"])

                return {"name_of_the_settlement": self.__district,
                        "oo": self.__oo,
                        "percents": percents,
                        "count_of_all_students": count_of_students}

    def get_report(self):
        if self.__report_type == 0:
            return self.__statistics_of_marks()

        elif self.__report_type == 1:
            return self.__comparison_of_ratings()
