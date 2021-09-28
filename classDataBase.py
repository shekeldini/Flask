import math
import sqlite3
import time


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def getAdminMenu(self):
        sql = '''SELECT * FROM adminmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def addUser(self, name, email, psw):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False
            tm = math.floor(time.time())
            self.__cur.execute(f"INSERT INTO users VALUES (NULL, ?, ?, ?, NULL, ?)", (name, email, psw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добовления пользователя в ДБ " + str(e))
            return False
        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()

            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

        return False

    def addPost(self, title, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?)", (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True

    def getPost(self, id_post):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE id = {id_post} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))
        return False, False

    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД " + str(e))
        return []

    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления аватара в БД: " + str(e))
            return False
        return True

    def deletePost(self, id_post):
        try:
            self.__cur.execute(f"DELETE FROM posts WHERE id = {id_post}")
            res = self.__cur.fetchone()
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print("Ошибка при удалении статьи из БД " + str(e))
        return False

    def getListUsers(self):
        try:
            self.__cur.execute(f"SELECT id, name, email FROM users ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД " + str(e))
        return []

    def deleteUser(self, id):
        try:
            self.__cur.execute(f"DELETE FROM users WHERE id = {id}")
            res = self.__cur.fetchone()
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print("Ошибка при удалении учетной записи из БД " + str(e))
        return False
