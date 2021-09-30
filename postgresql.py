import psycopg2
import time
import math
import openpyxl
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from glob import glob
from config import *
from vpr_analysis import VPR


class Postgresql:
    def __init__(self, connection):
        self.connection = connection
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self._cur = self.connection.cursor()

    def get_guest_menu(self):
        sql = '''SELECT * FROM guestmenu'''
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def get_logged_menu(self):
        sql = '''SELECT * FROM loggedmenu'''
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def get_admin_menu(self):
        sql = '''SELECT * FROM adminmenu'''
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def add_user(self, name, email, psw):
        try:
            self._cur.execute(f"SELECT COUNT(*) as count FROM users WHERE email LIKE '{email}'")
            res = self._cur.fetchone()
            if res[0] > 0:
                print("Пользователь с таким email уже существует")
                return False
            tm = math.floor(time.time())
            self._cur.execute(
                f"INSERT INTO users (name, email, psw, avatar, time) VALUES ('{name}', '{email}', '{psw}', NULL, {tm})")
        except psycopg2.Error as e:
            print("Ошибка добовления пользователя в ДБ " + str(e))
            return False
        return True

    def get_user(self, user_id):
        try:
            self._cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self._cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

        return False

    def get_user_by_email(self, email):
        try:
            self._cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self._cur.fetchone()

            if not res:
                print("Пользователь не найден")
                return False

            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

        return False

    def update_user_avatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = psycopg2.Binary(avatar)
            self._cur.execute(f"UPDATE users SET avatar = {binary} WHERE id = {user_id}")
        except psycopg2.Error as e:
            print("Ошибка обновления аватара в БД: " + str(e))
            return False
        return True

    def get_list_users(self):
        try:
            self._cur.execute(f"SELECT id, name, email FROM users ORDER BY time DESC")
            res = self._cur.fetchall()
            if res:
                return res
        except psycopg2.Error as e:
            print("Ошибка получения статей из БД " + str(e))
        return []

    def delete_user(self, id):
        try:
            self._cur.execute(f"DELETE FROM users WHERE id = {id}")
            return True
        except psycopg2.Error as e:
            print("Ошибка при удалении учетной записи из БД " + str(e))
        return False

    def get_districts(self):
        try:
            self._cur.execute(
                f'SELECT id_district, district_name FROM district ORDER BY id_district')
            res = self._cur.fetchall()
            if res:
                return res
        except psycopg2.Error as e:
            print("Ошибка получения муниципалитетов из БД " + str(e))
        return []

    def get_id_districts(self, district_name):
        try:
            self._cur.execute(
                f"SELECT id_district FROM district WHERE district_name = '{district_name.replace(' ', '_').replace('-', '_')}'")
            res, = self._cur.fetchone()
            if res:
                return res
        except psycopg2.Error as e:
            print("Ошибка получения id_districts из БД " + str(e))
        return []

    def get_id_name_of_the_settlement_by_id_district(self, id_district):
        try:
            self._cur.execute(
                f'SELECT id_name_of_the_settlement FROM name_of_the_settlement WHERE id_district = {id_district}')
            res = [i[0] for i in self._cur.fetchall()]

            if not res:
                print("Наименование населенного пункта не найдено")
                return []

            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_name_of_the_settlement(self, id_district, id_oo_location_type, name):
        try:
            self._cur.execute(
                f"SELECT id_name_of_the_settlement FROM name_of_the_settlement WHERE id_district = {id_district} AND"
                f" id_oo_location_type = {id_oo_location_type} AND"
                f" name = '{name}'")
            res, = self._cur.fetchone()
            if not res:
                print("id_name_of_the_settlement не найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_organizational_and_legal_form(self, type_of_organizational_and_legal_form):
        try:
            self._cur.execute(
                f"SELECT id_organizational_and_legal_form FROM organizational_and_legal_form WHERE "
                f"type_of_organizational_and_legal_form = '{type_of_organizational_and_legal_form[3:].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(', '(')}'")
            res, = self._cur.fetchone()
            if not res:
                print("id_organizational_and_legal_form не найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_oo_by_id_name_of_the_settlement(self, id_name_of_the_settlement):
        try:
            self._cur.execute(
                f'SELECT id_oo, oo_name FROM oo WHERE id_name_of_the_settlement = {id_name_of_the_settlement}')
            res = self._cur.fetchall()

            if not res:
                print("ОО не найдено")
                return []

            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_oo_from_district(self, id_district):
        try:
            list_id = self.get_id_name_of_the_settlement_by_id_district(id_district)
            res = []
            for id in list_id:
                list_oo = self.get_oo_by_id_name_of_the_settlement(id)
                if list_oo:
                    res.append(list_oo)
            if not res:
                print("ОО не были найдены")
                return []

            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_population_of_the_settlement(self, interval):
        try:
            interval = interval[3:].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(', '(')
            self._cur.execute(
                f"SELECT id_population_of_the_settlement FROM population_of_the_settlement WHERE interval = '{interval}'")
            res, = self._cur.fetchone()
            if not res:
                print("id_population_of_the_settlement не был найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_internet_speed(self, interval):
        try:
            interval = interval.strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(', '(')
            self._cur.execute(
                f"SELECT id_internet_speed FROM internet_speed WHERE interval = '{interval}'")
            res, = self._cur.fetchone()
            if not res:
                print("id_internet_speed не был найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_count_of_parents_attending_events(self, description):
        try:
            if description is None:
                description = "4.Нет_данных"
            description = description[2:].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(',
                                                                                                               '(')
            self._cur.execute(
                f"SELECT id_count_of_parents_attending_events FROM count_of_parents_attending_events WHERE description = '{description}'")
            res, = self._cur.fetchone()
            if not res:
                print("id_count_of_parents_attending_events не был найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_count_of_parents_ready_to_help(self, description):
        try:
            if description is None:
                description = "4.Нет_данных"
            description = description[2:].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(',
                                                                                                               '(')
            self._cur.execute(
                f"SELECT id_count_of_parents_ready_to_help FROM count_of_parents_ready_to_help WHERE description = '{description}'")
            res, = self._cur.fetchone()
            if not res:
                print("id_count_of_parents_ready_to_help не был найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_regular_transport_link(self, description):
        try:
            if description is None:
                description = "5. Нет_данных"
            description = description[3:].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(',
                                                                                                               '(')
            self._cur.execute(
                f"SELECT id_regular_transport_link FROM regular_transport_link WHERE description = '{description}'")
            res, = self._cur.fetchone()
            if not res:
                print("id_regular_transport_link не был найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_frequency_of_regular_transport_link(self, description):
        try:
            if description is None:
                description = "5. Нет_данных"
            description = description[3:].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(',
                                                                                                               '(')
            self._cur.execute(
                f"SELECT id_frequency_of_regular_transport_link FROM frequency_of_regular_transport_link WHERE description = '{description}'")
            res, = self._cur.fetchone()
            if not res:
                print("id_frequency_of_regular_transport_link не был найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_possibility_to_get_to_the_oo_by_public_transport(self, description):
        try:
            if description is None:
                description = "5. Нет_данных"
            description = description[3:].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(',
                                                                                                               '(')
            self._cur.execute(
                f"SELECT id_possibility_to_get_to_the_oo_by_public_transport FROM possibility_to_get_to_the_oo_by_public_transport WHERE description = '{description}'")
            res, = self._cur.fetchone()
            if not res:
                print("id_possibility_to_get_to_the_oo_by_public_transport не был найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_the_involvement_of_students_in_additional_education(self, interval) -> list:
        try:
            if interval is None:
                interval = "5. Нет даннных"
            interval = interval[3:].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(', '(')
            self._cur.execute(
                f"SELECT id_the_involvement_of_students_in_additional_education FROM the_involvement_of_students_in_additional_education WHERE interval = '{interval}'")
            res, = self._cur.fetchone()
            if not res:
                print("id_internet_speed не был найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_oo(self, oo_login):
        try:
            self._cur.execute(
                f"SELECT id_oo FROM oo WHERE oo_login = '{oo_login}'")
            res, = self._cur.fetchone()
            if not res:
                print("id_oo не был найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_subjects(self, subject_name):
        try:
            self._cur.execute(
                f"SELECT id_subjects FROM subjects WHERE subject_name = '{subject_name}'")
            res, = self._cur.fetchone()
            if not res:
                print("id_subjects не был найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_oo_parallels(self, parallel, id_oo):
        try:
            self._cur.execute(
                f"SELECT id_oo_parallels FROM oo_parallels WHERE parallel = {parallel} AND id_oo = {id_oo}")
            res, = self._cur.fetchone()
            if not res:
                print("id_oo_parallels не был найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_classes(self, id_oo_parallels, liter):
        try:
            self._cur.execute(
                f"SELECT id_classes FROM classes WHERE id_oo_parallels = {id_oo_parallels} AND liter = '{liter}'")
            res, = self._cur.fetchone()
            if not res:
                print("id_classes не был найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def get_id_textbooks(self, id_subjects, name):
        try:
            self._cur.execute(
                f"SELECT id_textbooks FROM textbooks WHERE id_subjects = {id_subjects} AND name = '{name}'")
            res = self._cur.fetchone()
            if not res:
                print("id_textbooks не был найден")
                print(id_subjects, name)
                self._cur.execute(
                    f"SELECT id_textbooks FROM textbooks WHERE id_subjects = {id_subjects} AND name = '{'Нет данных'}'")
                res = self._cur.fetchone()
            res, = res
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))


class FillDb(Postgresql):
    def __init__(self, connection):
        super().__init__(connection)

    def dropAllTables(self):
        try:
            self._cur.execute("DROP SCHEMA public CASCADE;")
            print("All Tables Drop")
        except psycopg2.Error as e:
            print("Ошибка: " + str(e))

    def createTables(self):
        try:
            self._cur.execute("CREATE SCHEMA IF NOT EXISTS public AUTHORIZATION admin;")
            self._cur.execute(open("sql\Create Tables SQL.sql", "r").read())
            print("Tables Created")
        except psycopg2.Error as e:
            print("Ошибка: " + str(e))

    def fill_district(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/logins.xlsx", data_only=True)
            data_sheet = data.active
            district_list = []
            for row in range(2, data_sheet.max_row + 1):
                district_value = data_sheet["C" + str(row)].value
                if district_value not in district_list:
                    district_list.append(district_value)
            for district_name in sorted(district_list):
                self._cur.execute(
                    f"INSERT INTO district (district_name) VALUES ('{district_name.replace(' ', '_').replace('-', '_')}')")
            print("Таблица district заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def find_district_id_by_district_name(self, district_name):
        try:
            district_name = district_name.replace(' ', '_').replace('-', '_')
            self._cur.execute(
                f"SELECT id_district FROM district WHERE district_name = '{district_name}'")
            res, = self._cur.fetchone()
            if not res:
                print("Район не найден")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def fill_oo_location_type(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active
            oo_location_type_list = []
            for row in range(2, data_sheet.max_row + 1):
                oo_location_type = data_sheet["N" + str(row)].value
                add_list = [oo_location_type[0], oo_location_type[2:]]
                if add_list not in oo_location_type_list:
                    oo_location_type_list.append(add_list)
            for location_type in sorted(oo_location_type_list, key=lambda x: x[0]):
                self._cur.execute(
                    f"INSERT INTO oo_location_type (location_type) VALUES ('"
                    f"{location_type[1].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(', '(')}')")
            print("Таблица oo_location_type заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def find_oo_location_type_id_by_location_type(self, location_type):
        try:
            location_type = location_type[2:]
            location_type = location_type.strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(',
                                                                                                               '(')
            self._cur.execute(
                f"SELECT id_oo_location_type FROM oo_location_type WHERE location_type = '{location_type}'")
            res, = self._cur.fetchone()
            if not res:
                print("Не найден тип расположения ОО")
                return []
            return res
        except psycopg2.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

    def fill_name_of_the_settlement(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active

            login_data = openpyxl.reader.excel.load_workbook(
                filename="excel/logins.xlsx", data_only=True)
            login_data_sheet = login_data.active
            data_list = []
            for data_row in range(2, data_sheet.max_row + 1):
                login_value = data_sheet["A" + str(data_row)].value
                for login_row in range(2, login_data_sheet.max_row + 1):
                    if login_data_sheet["A" + str(login_row)].value == login_value:
                        district_id = self.find_district_id_by_district_name(
                            login_data_sheet["C" + str(login_row)].value)
                        oo_location_type_id = self.find_oo_location_type_id_by_location_type(
                            data_sheet["N" + str(data_row)].value)
                        name = data_sheet["O" + str(data_row)].value
                        add_list = [district_id, oo_location_type_id, name]
                        if add_list not in data_list:
                            data_list.append(add_list)
            for lst in data_list:
                id_district, id_oo_location_type, name = lst
                self._cur.execute(
                    f"INSERT INTO name_of_the_settlement (id_district, id_oo_location_type, name) VALUES ({id_district}, {id_oo_location_type}, '{name}')")
            data.close()
            login_data.close()
            print("Таблица name_of_the_settlement заполненна ")
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def create_menu(self):
        try:
            self._cur.execute(f"INSERT INTO guestmenu (title,url) VALUES ('Главная', '/')")
            self._cur.execute(f"INSERT INTO guestmenu (title,url) VALUES ('Авторизация', '/login')")
            self._cur.execute(f"INSERT INTO loggedmenu (title,url) VALUES ('Главная', '/')")
            self._cur.execute(f"INSERT INTO loggedmenu (title,url) VALUES ('Аналтика ВПР', '/vpr_analysis')")
            self._cur.execute(f"INSERT INTO loggedmenu (title,url) VALUES ('Профиль', '/profile')")
            print("Меню созданно")
        except psycopg2.Error as e:
            print("Ошибка при создании меню " + str(e))
        return False

    def fill_organizational_and_legal_form(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active
            organizational_and_legal_form_list = []
            for row in range(2, data_sheet.max_row + 1):
                organizational_and_legal_form = data_sheet["I" + str(row)].value
                add_list = [organizational_and_legal_form[0], organizational_and_legal_form[2:]]
                if add_list not in organizational_and_legal_form_list:
                    organizational_and_legal_form_list.append(add_list)
            for type_of_organizational_and_legal_form in sorted(organizational_and_legal_form_list, key=lambda x: x[0]):
                self._cur.execute(
                    f"INSERT INTO organizational_and_legal_form (type_of_organizational_and_legal_form) VALUES ('"
                    f"{type_of_organizational_and_legal_form[1].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(', '(')}')")
            print("Таблица organizational_and_legal_form заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_oo_logins(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active
            oo_logins_list = []
            for row in range(2, data_sheet.max_row + 1):
                oo_logins = data_sheet["A" + str(row)].value
                if oo_logins not in oo_logins_list:
                    oo_logins_list.append(oo_logins)
            for login in oo_logins_list:
                self._cur.execute(
                    f"INSERT INTO oo_logins (oo_login) VALUES ('{login.strip()}')")
            print("Таблица oo_logins заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_population_of_the_settlement(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active
            population_of_the_settlement_list = []
            for row in range(2, data_sheet.max_row + 1):
                population_of_the_settlement = data_sheet["P" + str(row)].value
                add_list = [population_of_the_settlement[0], population_of_the_settlement[2:]]
                if add_list not in population_of_the_settlement_list:
                    population_of_the_settlement_list.append(add_list)
            for interval in sorted(population_of_the_settlement_list, key=lambda x: x[0]):
                self._cur.execute(
                    f"INSERT INTO population_of_the_settlement (interval) VALUES ('"
                    f"{interval[1].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(', '(')}')")
            print("Таблица population_of_the_settlement заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_internet_speed(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active
            internet_speed_list = []
            for row in range(2, data_sheet.max_row + 1):
                internet_speed = data_sheet["BR" + str(row)].value
                if internet_speed not in internet_speed_list:
                    internet_speed_list.append(internet_speed)
            internet_speed_list[1], internet_speed_list[3] = internet_speed_list[3], internet_speed_list[1]
            internet_speed_list[2], internet_speed_list[3] = internet_speed_list[3], internet_speed_list[2]

            for interval in internet_speed_list:
                self._cur.execute(
                    f"INSERT INTO internet_speed (interval) VALUES ('"
                    f"{interval.strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(', '(')}')")
            print("Таблица internet_speed заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_the_involvement_of_students_in_additional_education(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active
            the_involvement_of_students_in_additional_education_list = []
            for row in range(2, data_sheet.max_row + 1):
                the_involvement_of_students_in_additional_education = data_sheet["BS" + str(row)].value
                if the_involvement_of_students_in_additional_education not in the_involvement_of_students_in_additional_education_list:
                    the_involvement_of_students_in_additional_education_list.append(
                        the_involvement_of_students_in_additional_education)

            for interval in the_involvement_of_students_in_additional_education_list:
                if interval is None:
                    interval = "5. Нет даннных"
                self._cur.execute(
                    f"INSERT INTO the_involvement_of_students_in_additional_education (interval) VALUES ('"
                    f"{interval[3:].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(', '(')}')")
            print("Таблица the_involvement_of_students_in_additional_education заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_count_of_parents_attending_events(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active
            count_of_parents_attending_events_list = []
            for row in range(2, data_sheet.max_row + 1):
                count_of_parents_attending_events = data_sheet["CD" + str(row)].value
                if count_of_parents_attending_events is None:
                    count_of_parents_attending_events = "4. Нет_данных"
                add_list = [count_of_parents_attending_events[0], count_of_parents_attending_events[2:]]
                if add_list not in count_of_parents_attending_events_list:
                    count_of_parents_attending_events_list.append(add_list)
            for description in sorted(count_of_parents_attending_events_list, key=lambda x: x[0]):
                self._cur.execute(
                    f"INSERT INTO count_of_parents_attending_events (description) VALUES ('"
                    f"{description[1].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(', '(')}')")
            print("Таблица count_of_parents_attending_events заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_count_of_parents_ready_to_help(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active
            count_of_parents_ready_to_help_list = []
            for row in range(2, data_sheet.max_row + 1):
                count_of_parents_ready_to_help = data_sheet["CE" + str(row)].value
                if count_of_parents_ready_to_help is None:
                    count_of_parents_ready_to_help = "4. Нет_данных"
                add_list = [count_of_parents_ready_to_help[0], count_of_parents_ready_to_help[2:]]
                if add_list not in count_of_parents_ready_to_help_list:
                    count_of_parents_ready_to_help_list.append(add_list)
            for description in sorted(count_of_parents_ready_to_help_list, key=lambda x: x[0]):
                self._cur.execute(
                    f"INSERT INTO count_of_parents_ready_to_help (description) VALUES ('"
                    f"{description[1].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(', '(')}')")
            print("Таблица count_of_parents_ready_to_help заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_regular_transport_link(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active
            regular_transport_link_list = []
            for row in range(2, data_sheet.max_row + 1):
                regular_transport_link = data_sheet["Q" + str(row)].value
                if regular_transport_link is None:
                    regular_transport_link = "5. Нет_данных"
                add_list = [regular_transport_link[0], regular_transport_link[2:]]
                if add_list not in regular_transport_link_list:
                    regular_transport_link_list.append(add_list)
            for description in sorted(regular_transport_link_list, key=lambda x: x[0]):
                self._cur.execute(
                    f"INSERT INTO regular_transport_link (description) VALUES ('"
                    f"{description[1].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(', '(')}')")
            print("Таблица regular_transport_link заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_frequency_of_regular_transport_link(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active
            frequency_of_regular_transport_link_list = []
            for row in range(2, data_sheet.max_row + 1):
                frequency_of_regular_transport_link = data_sheet["R" + str(row)].value
                if frequency_of_regular_transport_link is None:
                    frequency_of_regular_transport_link = "5. Нет_данных"
                add_list = [frequency_of_regular_transport_link[0], frequency_of_regular_transport_link[2:]]
                if add_list not in frequency_of_regular_transport_link_list:
                    frequency_of_regular_transport_link_list.append(add_list)
            for description in sorted(frequency_of_regular_transport_link_list, key=lambda x: x[0]):
                self._cur.execute(
                    f"INSERT INTO frequency_of_regular_transport_link (description) VALUES ('"
                    f"{description[1].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(', '(')}')")
            print("Таблица frequency_of_regular_transport_link заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_possibility_to_get_to_the_oo_by_public_transport(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active
            possibility_to_get_to_the_oo_by_public_transport_list = []
            for row in range(2, data_sheet.max_row + 1):
                possibility_to_get_to_the_oo_by_public_transport = data_sheet["S" + str(row)].value
                if possibility_to_get_to_the_oo_by_public_transport is None:
                    possibility_to_get_to_the_oo_by_public_transport = "5. Нет_данных"
                add_list = [possibility_to_get_to_the_oo_by_public_transport[0],
                            possibility_to_get_to_the_oo_by_public_transport[2:]]
                if add_list not in possibility_to_get_to_the_oo_by_public_transport_list:
                    possibility_to_get_to_the_oo_by_public_transport_list.append(add_list)
            for description in sorted(possibility_to_get_to_the_oo_by_public_transport_list, key=lambda x: x[0]):
                self._cur.execute(
                    f"INSERT INTO possibility_to_get_to_the_oo_by_public_transport (description) VALUES ('"
                    f"{description[1].strip().replace(' ', '_').replace('-', '_').replace(',', '').replace('_(', '(')}')")
            print("Таблица possibility_to_get_to_the_oo_by_public_transport заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_oo(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active

            login_data = openpyxl.reader.excel.load_workbook(
                filename="excel/logins.xlsx", data_only=True)
            login_data_sheet = login_data.active
            login_region = {}
            for row in range(2, login_data_sheet.max_row + 1):
                login = login_data_sheet["A" + str(row)].value
                region = login_data_sheet["C" + str(row)].value

                if login_region.get(region) is None:
                    login_region[region] = [login]
                else:
                    login_region[region].append(login)
            for row in range(2, data_sheet.max_row + 1):
                oo_login = data_sheet["A" + str(row)].value
                year = "2021"
                for region_d, login_d in login_region.items():
                    if oo_login in login_d:
                        id_name_of_the_settlement = self.get_id_name_of_the_settlement(
                            self.get_id_districts(region_d),
                            self.find_oo_location_type_id_by_location_type(data_sheet["N" + str(row)].value),
                            data_sheet["O" + str(row)].value)
                id_organizational_and_legal_form = self.get_id_organizational_and_legal_form(
                    data_sheet["I" + str(row)].value)
                id_population_of_the_settlement = self.get_id_population_of_the_settlement(
                    data_sheet["P" + str(row)].value)
                id_internet_speed = self.get_id_internet_speed(data_sheet["BR" + str(row)].value)
                id_the_involvement_of_students_in_additional_education = self.get_id_the_involvement_of_students_in_additional_education(
                    data_sheet["BS" + str(row)].value)
                id_count_of_parents_attending_events = self.get_id_count_of_parents_attending_events(
                    data_sheet["CD" + str(row)].value)
                id_count_of_parents_ready_to_help = self.get_id_count_of_parents_ready_to_help(
                    data_sheet["CE" + str(row)].value)
                id_regular_transport_link = self.get_id_regular_transport_link(data_sheet["Q" + str(row)].value)
                id_frequency_of_regular_transport_link = self.get_id_frequency_of_regular_transport_link(
                    data_sheet["R" + str(row)].value)
                id_possibility_to_get_to_the_oo_by_public_transport = self.get_id_possibility_to_get_to_the_oo_by_public_transport(
                    data_sheet["S" + str(row)].value)
                oo_name = data_sheet["C" + str(row)].value
                oo_full_name = data_sheet["D" + str(row)].value
                oo_address = data_sheet["E" + str(row)].value
                full_name_of_the_director = data_sheet["F" + str(row)].value
                email_oo = data_sheet["H" + str(row)].value
                phone_number = str(data_sheet["G" + str(row)].value).replace("(", "").replace(")", "").replace("-", "")
                oo_is_corrective = True if data_sheet["T" + str(row)].value == "Да" else False
                oo_is_night = True if data_sheet["U" + str(row)].value == "Да" else False
                oo_is_special_educational_institution_of_a_closed_type = True if data_sheet["V" + str(
                    row)].value == "Да" else False
                oo_attached_to_an_organization_executing_a_sentence_of_imprisonment = True if data_sheet["W" + str(
                    row)].value == "Да" else False
                oo_is_a_boarding = True if data_sheet["X" + str(row)].value == "Да" else False
                count_of_teachers = data_sheet["BA" + str(row)].value if data_sheet["BA" + str(row)].value else 0
                count_of_teachers_of_the_highest_category = data_sheet["BB" + str(row)].value if data_sheet[
                    "BB" + str(row)].value else 0
                count_of_teachers_not_older_than_30_years = data_sheet["BC" + str(row)].value if data_sheet[
                    "BC" + str(row)].value else 0
                count_of_teachers_reached_retirement_age = data_sheet["BD" + str(row)].value if data_sheet[
                    "BD" + str(row)].value else 0
                count_of_classrooms_in_which_classes_are_held = data_sheet["BL" + str(row)].value if data_sheet[
                    "BL" + str(row)].value else 0
                count_of_classrooms_in_which_the_teacher_place_is_equipped_with_a_computer = data_sheet[
                    "BM" + str(row)].value if data_sheet["BM" + str(row)].value else 0
                count_of_cabinets_with_a_projector_or_interactive_whiteboard = data_sheet["BN" + str(row)].value if \
                    data_sheet["BN" + str(row)].value else 0
                count_of_computers_that_students_can_use_in_the_learning_process = data_sheet["BO" + str(row)].value if \
                    data_sheet["BO" + str(row)].value else 0
                count_of_old_computers = data_sheet["BP" + str(row)].value if data_sheet["BP" + str(row)].value else 0
                count_of_computers_with_internet_access = data_sheet["BQ" + str(row)].value if data_sheet[
                    "BQ" + str(row)].value else 0
                self._cur.execute(
                    f"INSERT INTO oo (oo_login,"
                    f" year,"
                    f"id_name_of_the_settlement,"
                    f"id_organizational_and_legal_form,"
                    f"id_population_of_the_settlement,"
                    f"id_internet_speed,"
                    f"id_the_involvement_of_students_in_additional_education,"
                    f"id_count_of_parents_attending_events,"
                    f"id_count_of_parents_ready_to_help,"
                    f"id_regular_transport_link,"
                    f"id_frequency_of_regular_transport_link,"
                    f"id_possibility_to_get_to_the_oo_by_public_transport,"
                    f"oo_name,"
                    f"oo_full_name,"
                    f"oo_address,"
                    f"full_name_of_the_director,"
                    f"email_oo,"
                    f"phone_number,"
                    f"oo_is_corrective,"
                    f"oo_is_night,"
                    f"oo_is_special_educational_institution_of_a_closed_type,"
                    f"oo_attached_to_an_organization_executing_a_sentence_of_imprisonment,"
                    f"oo_is_a_boarding,"
                    f"count_of_teachers,"
                    f"count_of_teachers_of_the_highest_category,"
                    f"count_of_teachers_not_older_than_30_years,"
                    f"count_of_teachers_reached_retirement_age,"
                    f"count_of_classrooms_in_which_classes_are_held,"
                    f"count_of_classrooms_in_which_the_teacher_place_is_equipped_with_a_computer,"
                    f"count_of_cabinets_with_a_projector_or_interactive_whiteboard,"
                    f"count_of_computers_that_students_can_use_in_the_learning_process,"
                    f"count_of_old_computers,"
                    f"count_of_computers_with_internet_access) VALUES ('{oo_login}',"
                    f"'{year}',"
                    f"{id_name_of_the_settlement},"
                    f"{id_organizational_and_legal_form},"
                    f"{id_population_of_the_settlement},"
                    f"{id_internet_speed},"
                    f"{id_the_involvement_of_students_in_additional_education},"
                    f"{id_count_of_parents_attending_events},"
                    f"{id_count_of_parents_ready_to_help},"
                    f" {id_regular_transport_link},"
                    f" {id_frequency_of_regular_transport_link},"
                    f" {id_possibility_to_get_to_the_oo_by_public_transport},"
                    f" '{oo_name}',"
                    f" '{oo_full_name}',"
                    f" '{oo_address}',"
                    f" '{full_name_of_the_director}',"
                    f" '{email_oo}',"
                    f" '{phone_number}',"
                    f" {oo_is_corrective},"
                    f" {oo_is_night},"
                    f" {oo_is_special_educational_institution_of_a_closed_type},"
                    f" {oo_attached_to_an_organization_executing_a_sentence_of_imprisonment},"
                    f" {oo_is_a_boarding},"
                    f" {count_of_teachers},"
                    f" {count_of_teachers_of_the_highest_category},"
                    f" {count_of_teachers_not_older_than_30_years},"
                    f" {count_of_teachers_reached_retirement_age},"
                    f" {count_of_classrooms_in_which_classes_are_held},"
                    f" {count_of_classrooms_in_which_the_teacher_place_is_equipped_with_a_computer},"
                    f" {count_of_cabinets_with_a_projector_or_interactive_whiteboard},"
                    f" {count_of_computers_that_students_can_use_in_the_learning_process},"
                    f" {count_of_old_computers},"
                    f" {count_of_computers_with_internet_access})")
            print("Таблица ОО заполненна")
            data.close()
            login_data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_duration_of_refresher_courses(self):
        try:
            for values in ["Длительностью_не_более_36_часов",
                           "Длительностью_более_36_часов_и_не_более_72_часов",
                           "Длительностью_более_72_часов"]:
                self._cur.execute(f"INSERT INTO duration_of_refresher_courses (duration) VALUES ('{values}')")
            print("Таблица duration_of_refresher_courses заполненна")
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_completed_advanced_training_courses_for_teachers(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active
            for row in range(2, data_sheet.max_row + 1):
                count_of_teachers_36h = data_sheet["BE" + str(row)].value if data_sheet["BE" + str(row)].value else 0
                count_of_teachers_36h_72h = data_sheet["BF" + str(row)].value if data_sheet[
                    "BF" + str(row)].value else 0
                count_of_teachers_72h = data_sheet["BG" + str(row)].value if data_sheet["BG" + str(row)].value else 0
                oo_login = self.get_id_oo(data_sheet["A" + str(row)].value)

                for id_duration, count_of_teachers in zip([1, 2, 3, 4],
                                                          [count_of_teachers_36h, count_of_teachers_36h_72h,
                                                           count_of_teachers_72h]):
                    self._cur.execute(f"INSERT INTO completed_advanced_training_courses_for_teachers ("
                                      f" id_oo,"
                                      f" id_duration_of_refresher_courses,"
                                      f" count_of_teachers)"
                                      f" VALUES ({oo_login}, {id_duration}, {count_of_teachers})")
            print("Таблица completed_advanced_training_courses_for_teachers заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_description_of_work_with_teachers_taking_advanced_training_courses(self):
        try:
            for values in ["Их_сопровождает_методслужба_муниципалитета",
                           "Они_делятся_опытом_в_рамках_профессионального_общения_с_коллегами_в_школе",
                           "Они_самостоятельно_отрабатывают_полученные_навыки_на_уроках",
                           "никак"]:
                self._cur.execute(
                    f"INSERT INTO description_of_work_with_teachers_taking_advanced_training_courses (description) VALUES ('{values}')")
            print("Таблица description_of_work_with_teachers_taking_advanced_training_courses заполненна")
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_work_with_teachers_taking_advanced_training_courses(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active
            for row in range(2, data_sheet.max_row + 1):
                description_1 = data_sheet["BH" + str(row)].value if data_sheet["BH" + str(row)].value else "Нет_данных"
                description_2 = data_sheet["BI" + str(row)].value if data_sheet["BI" + str(row)].value else "Нет_данных"
                description_3 = data_sheet["BJ" + str(row)].value if data_sheet["BJ" + str(row)].value else "Нет_данных"
                description_4 = data_sheet["BK" + str(row)].value if data_sheet["BK" + str(row)].value else "Нет_данных"
                oo_login = self.get_id_oo(data_sheet["A" + str(row)].value)
                for id_description, description in zip([1, 2, 3, 4],
                                                       [description_1, description_2, description_3, description_4]):
                    self._cur.execute(f"INSERT INTO completed_advanced_training_courses_for_teachers ("
                                      f" id_oo,"
                                      f" id_duration_of_refresher_courses,"
                                      f" value)"
                                      f" VALUES ({oo_login}, {id_description}, '{description}')")
            print("Таблица work_with_teachers_taking_advanced_training_courses заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_description_of_career_guidance(self):
        try:
            for values in ["Рассказ о профессиях во время классных часов",
                           "Беседы с представителями различных профессий",
                           "Лекции сотрудников службы занятости",
                           "Психологические тестирования построение профессиограмм",
                           "Экскурсии в организации на производства",
                           "Участие в профориентационных проектах",
                           "Практика на предприятиях"]:
                self._cur.execute(
                    f"INSERT INTO description_of_career_guidance (description) VALUES ('{values.replace(' ', '_')}')")
            print("Таблица description_of_career_guidance заполненна")
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_oo_description_of_career_guidance(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active
            for row in range(2, data_sheet.max_row + 1):
                description_1 = data_sheet["BU" + str(row)].value if data_sheet["BU" + str(row)].value else "Нет_данных"
                description_2 = data_sheet["BV" + str(row)].value if data_sheet["BV" + str(row)].value else "Нет_данных"
                description_3 = data_sheet["BW" + str(row)].value if data_sheet["BW" + str(row)].value else "Нет_данных"
                description_4 = data_sheet["BX" + str(row)].value if data_sheet["BX" + str(row)].value else "Нет_данных"
                description_5 = data_sheet["BY" + str(row)].value if data_sheet["BY" + str(row)].value else "Нет_данных"
                description_6 = data_sheet["BZ" + str(row)].value if data_sheet["BZ" + str(row)].value else "Нет_данных"
                description_7 = data_sheet["CA" + str(row)].value if data_sheet["CA" + str(row)].value else "Нет_данных"
                oo_login = self.get_id_oo(data_sheet["A" + str(row)].value)
                for id_description, description in zip([1, 2, 3, 4, 5, 6, 7],
                                                       [description_1, description_2, description_3, description_4,
                                                        description_5, description_6, description_7]):
                    self._cur.execute(f"INSERT INTO oo_description_of_career_guidance ("
                                      f" id_oo,"
                                      f" id_description_of_career_guidance,"
                                      f" value)"
                                      f" VALUES ({oo_login}, {id_description}, '{description}')")
            print("Таблица oo_description_of_career_guidance заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_levels_of_the_educational_program(self):
        try:
            for values in ["Начальное общее образование",
                           "Основное общее образование",
                           "Среднее общее образование",
                           "Среднее профессиональное образование"]:
                self._cur.execute(
                    f"INSERT INTO levels_of_the_educational_program (educational_program) VALUES ('{values.replace(' ', '_')}')")
            print("Таблица levels_of_the_educational_program заполненна")

        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_oo_levels_of_the_educational_program(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active
            for row in range(2, data_sheet.max_row + 1):
                lvl1 = data_sheet["J" + str(row)].value if data_sheet["J" + str(row)].value else "Нет_данных"
                lvl2 = data_sheet["K" + str(row)].value if data_sheet["K" + str(row)].value else "Нет_данных"
                lvl3 = data_sheet["L" + str(row)].value if data_sheet["L" + str(row)].value else "Нет_данных"
                lvl4 = data_sheet["M" + str(row)].value if data_sheet["M" + str(row)].value else "Нет_данных"
                oo_login = self.get_id_oo(data_sheet["A" + str(row)].value)
                for id_levels_of_the_educational_program, value in zip([1, 2, 3, 4],
                                                                       [lvl1, lvl2, lvl3, lvl4]):
                    self._cur.execute(f"INSERT INTO oo_levels_of_the_educational_program ("
                                      f" id_oo,"
                                      f" id_levels_of_the_educational_program,"
                                      f" value)"
                                      f" VALUES ({oo_login}, {id_levels_of_the_educational_program}, '{value}')")
            print("Таблица oo_levels_of_the_educational_program заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_percentage_of_parents_attending_parentteacher_meeting(self):
        try:
            data = openpyxl.reader.excel.load_workbook(
                filename="excel/Сбор контекстных данных об ОО и участниках ВПР 2021.xlsx", data_only=True)
            data_sheet = data.active
            for row in range(2, data_sheet.max_row + 1):
                lvl1 = data_sheet["CB" + str(row)].value if data_sheet["CB" + str(row)].value else 0
                lvl2 = data_sheet["CC" + str(row)].value if data_sheet["CC" + str(row)].value else 0
                lvl3 = data_sheet["CF" + str(row)].value if data_sheet["CF" + str(row)].value else 0
                oo_login = self.get_id_oo(data_sheet["A" + str(row)].value)
                for id_levels_of_the_educational_program, value in zip([1, 2, 3],
                                                                       [lvl1, lvl2, lvl3]):
                    self._cur.execute(f"INSERT INTO percentage_of_parents_attending_parentteacher_meeting ("
                                      f" id_oo,"
                                      f" id_levels_of_the_educational_program,"
                                      f" value)"
                                      f" VALUES ({oo_login}, {id_levels_of_the_educational_program}, {value})")
            print("Таблица percentage_of_parents_attending_parentteacher_meeting заполненна")
            data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_parallels(self):
        try:
            for value in [4, 5, 6, 7, 8, 10, 11]:
                self._cur.execute(
                    f"INSERT INTO parallels (parallel) VALUES ({value})")
            print("Таблица parallels заполненна")
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_oo_parallels(self):
        try:
            all_parallels = glob("excel/vpr_results/*")
            parallels_schools = {}
            for path in all_parallels:
                parallel = path[path.index("\\") + 1:]
                parallels_schools[int(parallel)] = set()
                subj_in_parallel = path.replace("\\", "/") + "/*"
                files = glob(subj_in_parallel)
                for file in files:
                    df = VPR(file)
                    parallels_schools[int(parallel)] |= set(df.get_unic_schools())
            for parallel in parallels_schools:
                for login in parallels_schools[parallel]:
                    id_oo = self.get_id_oo(login)
                    self._cur.execute(
                        f"INSERT INTO oo_parallels (parallel, id_oo) VALUES ({parallel}, {id_oo})")
            print("Таблица oo_parallels заполненна")

        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_subjects(self):
        try:
            subjects = ["Английский_язык", "Биология", "География", "История", "Математика", "Немецкий_язык",
                        "Обществознание", "Окружающий_мир", "Русский_язык", "Физика", "Французский_язык", "Химия"]
            for subject in subjects:
                self._cur.execute(
                    f"INSERT INTO subjects (subject_name) VALUES ('{subject}')")

            print("Таблица subjects заполненна")
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_textbooks(self):
        try:
            books_data = openpyxl.reader.excel.load_workbook(
                filename="excel/books.xlsx", data_only=True)
            books_sheet = books_data.active
            subj_dict = {"bio": "Биология", "de": "Немецкий_язык", "en": "Английский_язык", "fi": "Физика",
                         "fr": "Французский_язык", "geo": "География", "hi": "Химия", "him": "Химия", "is": "История",
                         "ma": "Математика", "ob": "Обществознание", "om": "Окружающий_мир", "ru": "Русский_язык"}
            for row in range(1, books_sheet.max_row + 1):
                book_key = books_sheet["A" + str(row)].value
                book_name = books_sheet["B" + str(row)].value
                for subj_key in subj_dict:
                    if subj_key in book_key:
                        subj_name = subj_dict[subj_key]
                        id_subjects = self.get_id_subjects(subj_name)

                self._cur.execute(
                    f"INSERT INTO textbooks (id_subjects, key, name) VALUES ({id_subjects}, '{book_key}', '{book_name.strip()}')")
            for id_subjects_ in range(1, 13):
                self._cur.execute(
                    f"INSERT INTO textbooks (id_subjects, key, name) VALUES ({id_subjects_}, '{'nan'}', '{'Нет данных'}')")
            print("Таблица textbooks заполненна")
            books_data.close()
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_classes(self):
        try:
            all_parallels = glob("excel/vpr_results/*")
            for path in all_parallels:
                result_dict = {}
                parallel = int(path[path.index("\\") + 1:])
                subj_in_parallel = path.replace("\\", "/") + "/*"
                files = glob(subj_in_parallel)
                for file in files:
                    df = VPR(file)
                    dict_schools_and_liters = df.get_dict_schools_liters()
                    for school in dict_schools_and_liters:
                        if result_dict.get(school) is None:
                            result_dict[school] = dict_schools_and_liters[school]
                        else:
                            for liter in dict_schools_and_liters[school]:
                                if liter not in result_dict[school]:
                                    result_dict[school].append(liter)
                for login in result_dict:
                    id_oo = self.get_id_oo(login)
                    id_oo_parallels = self.get_id_oo_parallels(parallel, id_oo)
                    for liter in result_dict[login]:
                        self._cur.execute(
                            f"INSERT INTO classes (id_oo_parallels, liter) VALUES ({id_oo_parallels}, '{liter}')")
            print("Таблица classes заполненна")

        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_classes_textbooks(self):
        try:
            all_parallels = glob("excel/vpr_results/*")
            result_dict = {}
            for path in all_parallels:
                parallel = int(path[path.index("\\") + 1:])
                subj_in_parallel = path.replace("\\", "/") + "/*"
                files = glob(subj_in_parallel)
                for file in files:
                    print(file.replace("\\", "/"))
                    df = VPR(file.replace("\\", "/"))
                    id_subjects = self.get_id_subjects(df.get_subj_name())
                    dict_books = df.get_dict_schools_liters_books()
                    if result_dict.get(parallel) is None:
                        result_dict[parallel] = {id_subjects: dict_books}
                    else:
                        if result_dict[parallel].get(id_subjects) is None:
                            result_dict[parallel][id_subjects] = dict_books
                        else:
                            for school in dict_books:
                                if result_dict[parallel][id_subjects].get(school) is None:
                                    result_dict[parallel][id_subjects][school] = dict_books[school]
                                else:
                                    for liter in dict_books[school]:
                                        if result_dict[parallel][id_subjects][school].get(liter) is None:
                                            result_dict[parallel][id_subjects][school][liter] = dict_books[school][
                                                liter]
            for parallel in result_dict:
                for id_subjects in result_dict[parallel]:
                    for login_school in result_dict[parallel][id_subjects]:
                        id_oo_parallels = self.get_id_oo_parallels(parallel, self.get_id_oo(login_school))
                        for liter in result_dict[parallel][id_subjects][login_school]:
                            book_name = result_dict[parallel][id_subjects][login_school][liter]
                            id_classes = self.get_id_classes(id_oo_parallels, liter)
                            id_textbooks = self.get_id_textbooks(id_subjects, book_name.strip())
                            self._cur.execute(
                                f"INSERT INTO classes_textbooks (id_classes, id_textbooks, id_oo_parallels) "
                                f"VALUES ({id_classes}, {id_textbooks}, {id_oo_parallels})")
            print("Таблица classes_textbooks заполненна")
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))

    def fill_students(self):
        try:
            all_parallels = glob("excel/vpr_results/*")
            result_dict = {}  # {parallel: {school: {liter: {students: gender}}}}
            for path in all_parallels:
                parallel = int(path[path.index("\\") + 1:])
                subj_in_parallel = path.replace("\\", "/") + "/*"
                files = glob(subj_in_parallel)
                for file in files:
                    print(file.replace("\\", "/"))
                    df = VPR(file.replace("\\", "/"))
                    dict_schools_liters_students = df.get_dict_schools_liters_students()  # {school: {liter: {students: gender}}}
                    if result_dict.get(parallel) is None:
                        result_dict[parallel] = dict_schools_liters_students
                    else:
                        for school in dict_schools_liters_students:
                            if result_dict[parallel].get(school) is None:
                                result_dict[parallel][school] = dict_schools_liters_students[school]
                            else:
                                for liter in dict_schools_liters_students[school]:
                                    if result_dict[parallel][school].get(liter) is None:
                                        result_dict[parallel][school][liter] = dict_schools_liters_students[school][liter]
                                    else:
                                        for student in dict_schools_liters_students[school][liter]:
                                            if result_dict[parallel][school][liter].get(student) is None:
                                                gender = dict_schools_liters_students[school][liter][student]
                                                result_dict[parallel][school][liter][student] = gender
            count = 0
            for parallel in result_dict:
                for school in result_dict[parallel]:
                    id_oo_parallels = self.get_id_oo_parallels(parallel, self.get_id_oo(school))
                    for liter in result_dict[parallel][school]:
                        count += len(result_dict[parallel][school][liter])
                        id_classes = self.get_id_classes(id_oo_parallels, liter)
                        for student in result_dict[parallel][school][liter]:
                            gender = result_dict[parallel][school][liter][student]
                            self._cur.execute(
                                f"INSERT INTO students (id_oo_parallels, id_classes, gender, student_number) "
                                f"VALUES ({id_oo_parallels}, {id_classes}, '{gender}', '{student}')")
            print(count)
            print("Таблица classes_textbooks заполненна")
        except psycopg2.Error as e:
            print("Ошибка при заполнении БД " + str(e))


psql = FillDb(psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT))
psql.dropAllTables()
psql.createTables()
psql.create_menu()
psql.fill_district()
psql.fill_oo_location_type()
psql.fill_name_of_the_settlement()
psql.fill_organizational_and_legal_form()
psql.fill_oo_logins()
psql.fill_population_of_the_settlement()
psql.fill_internet_speed()
psql.fill_the_involvement_of_students_in_additional_education()
psql.fill_count_of_parents_attending_events()
psql.fill_count_of_parents_ready_to_help()
psql.fill_regular_transport_link()
psql.fill_frequency_of_regular_transport_link()
psql.fill_possibility_to_get_to_the_oo_by_public_transport()
psql.fill_oo()
psql.fill_duration_of_refresher_courses()
psql.fill_completed_advanced_training_courses_for_teachers()
psql.fill_description_of_work_with_teachers_taking_advanced_training_courses()
psql.fill_description_of_career_guidance()
psql.fill_oo_description_of_career_guidance()
psql.fill_levels_of_the_educational_program()
psql.fill_oo_levels_of_the_educational_program()
psql.fill_percentage_of_parents_attending_parentteacher_meeting()
psql.fill_parallels()
psql.fill_oo_parallels()
psql.fill_subjects()
psql.fill_textbooks()
psql.fill_classes()
psql.fill_classes_textbooks()
psql.fill_students()
