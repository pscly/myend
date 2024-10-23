from flask import (
    Blueprint,
    redirect,
    request,
    g,
    render_template,
    render_template,
    jsonify,
    send_from_directory,
    url_for,
)
from entities import data_saves
from .. import myfuncs
import time
import random
from entities.mymongo import MyMongo1
from addict import Dict
from entities import data_saves
from utils.up_dns import up_dns1
from flask_login import login_user, logout_user, login_required, current_user
import os
from utils.core import hash_password, verify_password

from utils.login1 import (
    UserLogin,
    get_one_user,
    save_one_user,
    login_user as custom_login_user
)

service_name = "/"
bp = Blueprint(service_name, __name__)


@bp.route("/", methods=["GET"])
def index():
    data = myfuncs.get_datas(request)
    data_saves.save_data(data, 1, "gen")
    yyids = [28188427, 1407112865, 1919147134, 1453957944, 1886371886, 450853439]
    return render_template(
        "geng.html",
        yyid=random.choice(yyids),
        imgid=str(random.randint(1, 18)),
        beian=os.y.data2.BEIAN,
    )
    # return render_template('down.html', files=files, imgid=str(random.randint(1, 18)))
    # return render_template('down.html', datas={"files": files, "imgid": random.randint(1, 18)})


@bp.route("/robot.txt", methods=["GET"])
def robot():
    data = myfuncs.get_datas(request)
    data_saves.save_data(data, 1, "robot")
    return "User-agent: *\nDisallow: /"


@bp.route("/md", methods=["GET"])
def md():
    data = myfuncs.get_datas(request)
    data_saves.save_data(data, 1, "gen")
    return data


@bp.route("/emi/", methods=["GET", "POST"])
def emi():
    return redirect("/email/", request.base_url)


# 将 static/geng 文件夹下的文件列为跟目录下的文件(可以直接访问)
@bp.route("/<path:filename>", methods=["GET"])
def geng(filename):
    """
    todo: 上传文件处最好可以选择可以上传到此文件夹下 static/geng
    """
    return send_from_directory(os.path.join(os.y.static_folder, "geng"), filename)


@bp.route("/login", methods=["GET", "POST"])
def login(msg_txt="", error=""):
    if request.method == "POST":
        try:
            name = request.form.get("name")
            pwd = request.form.get("pwd")
            if not (name and pwd):
                return render_template("login.html", error="用户名或密码不全", r_txt="登 录")
            users = get_one_user(name)
            if users and verify_password(pwd, users.get("pwd")):
                user = User()
                user.id = name
                login_user(user)
                return redirect(url_for("/.index"))
            else:
                return render_template("login.html", error="用户名或密码错误", r_txt="登 录")
        except:
            return render_template("login.html", error="用户名或密码错误_特殊类型", r_txt="登 录")
    else:
        if current_user.is_authenticated:
            return redirect(url_for("/.index"))
        return render_template("login.html", r_txt="登 录", msg_txt=msg_txt, error=error)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("/.index"))


@bp.route("/reg", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        pwd = request.form.get("pwd")
        y_code = request.form.get("y_code")
        # if y_code != time.strftime("%H%M%d"):
        #     return render_template("login.html", error="邀请码错误", r_txt="注 册")
        if not (name and pwd):
            return render_template("login.html", error="用户名或密码不全", r_txt="注 册")
        users = get_one_user(name)
        if users:
            return render_template(
                "login.html", error="这个用户已经有了", r_txt="注 册"
            )
        else:
            users = Dict({"name": name, "pwd": hash_password(pwd), "is_ban": 0})
            save_one_user(users)
            login_user(users)   
            return redirect(url_for("/.index"))
    else:
        if current_user.is_authenticated:
            return redirect(url_for("/.index"))
        return render_template("login.html", r_txt="注 册")


@bp.route("/ok1", methods=["GET", "POST"])
def ok1():
    # 如果用户已经登录
    if current_user.is_authenticated:
        return jsonify({"msg": "login ok, 11111", "user": current_user.id})
    return '<h1>你没有登录</h1>\n<a herf="http://127.0.0.1/login">no 登录 </a>'
