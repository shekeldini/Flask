from flask import Blueprint, render_template, url_for, request, flash, session, redirect, abort, g, make_response
from forms import AdminForm
from werkzeug.security import check_password_hash
from classDataBase import DataBase

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')
db = None
dbase = None


@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for(".login"))

    return render_template('admin/index.html', title='Админ-панель', menu=dbase.getAdminMenu())


@admin.route('/listpubs')
def listpubs():
    if not isLogged():
        return redirect(url_for(".login"))
    return render_template('admin/listpubs.html', title='Админ-панель', menu=dbase.getAdminMenu(),
                           posts=dbase.getPostsAnonce())


@admin.route('/listusers')
def listusers():
    if not isLogged():
        return redirect(url_for(".login"))
    return render_template('admin/listusers.html', title='Админ-панель', menu=dbase.getAdminMenu(),
                           list=dbase.getListUsers())


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


@admin.before_request
def before_request():
    global db, dbase
    db = g.get('link_db')
    dbase = DataBase(db)


@admin.teardown_request
def teardown_request(request):
    global db, dbase
    db = None
    dbase = None


@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for(".index"))

    form = AdminForm()
    if form.validate_on_submit():
        user = dbase.getUserByEmail(form.email.data)
        if user['name'] == "admin" and user['email'] == "admin@a.c" and check_password_hash(user["psw"], form.psw.data):
            login_admin()
            return redirect(url_for(".index"))

        flash("Неверный логин или пароль", "error")
    return render_template('admin/login.html', title='Админ-панель', form=form)


@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if isLogged():
        logout_admin()
    return redirect(url_for('.login'))


@admin.route("/delete_post/<int:id_post>")
def delete_post(id_post):
    if dbase.deletePost(id_post):
        flash("Запись удалена", "success")
    else:
        flash("Ошибка при удалении статьи", "error")
    return redirect(url_for(".listpubs"))


@admin.route("/delete_user/<int:id>")
def delete_user(id):
    if dbase.deleteUser(id):
        flash("Запись удалена", "success")
    else:
        flash("Ошибка при удалении статьи", "error")
    return redirect(url_for(".listusers"))
