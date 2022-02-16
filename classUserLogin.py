from flask_login import UserMixin
from flask import url_for


class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.get_user(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return self.__user[0]

    def get_name(self):
        return self.__user[2] if self.__user[2] else "Гость"

    def get_login(self):
        return self.__user[1]

    def get_email(self):
        return self.__user[3] if self.__user[3] else ""

    def get_phone(self):
        return self.__user[4] if self.__user[4] else ""

    def get_id_role(self):
        return self.__user[7]

    def getAvatar(self, app):
        img = None
        if not self.__user[4]:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='images/default.png'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию: " + str(e))
        else:
            img = self.__user[4]

        return bytearray(img)

    def verifyExt(self, filename):
        ext = filename.rsplit('.', 1)[1]
        if ext == "png" or ext == "PNG" or ext == "jpg" or ext == "jpeg":
            return True
        return False
