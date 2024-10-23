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
    flash
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
from werkzeug.security import generate_password_hash
from datetime import datetime

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
        name = request.form.get("name")
        pwd = request.form.get("pwd")
        if not (name and pwd):
            flash("用户名或密码不全", "error")
            return render_template("login.html", r_txt="登 录")
        
        result, status_code = custom_login_user(name, pwd)
        if status_code == 200:
            flash("登录成功", "success")
            return redirect(url_for("/.index"))
        else:
            flash(result["message"], "error")
            return render_template("login.html", r_txt="登 录")
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
        
        # 输入验证
        if not (name and pwd):
            flash("用户名或密码不能为空", "error")
            return render_template("login.html", r_txt="注 册")
        
        # 用户名长度检查
        if len(name) < 3 or len(name) > 20:
            flash("用户名长度必须在3到20个字符之间", "error")
            return render_template("login.html", r_txt="注 册")
        
        # 密码复杂度检查
        if len(pwd) < 3:
            flash("密码长度必须至少为3个字符", "error")
            return render_template("login.html", r_txt="注 册")
        
        # 邀请码检查（如果需要）
        # if y_code != time.strftime("%H%M%d"):
        #     flash("邀请码错误", "error")
        #     return render_template("login.html", r_txt="注 册")
        
        users = get_one_user(name)
        if users:
            flash("用户名已存在", "error")
            return render_template("login.html", r_txt="注 册")
        
        # 创建新用户
        hashed_password = generate_password_hash(pwd)
        new_user = Dict({
            "name": name,
            "pwd": hashed_password,
            "is_ban": 0,
            "is_active": 0, # 是否被管理员激活
            "user_type": 0,  # 设置默认用户类型
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow()
        })
        if name == "pscly":
            new_user.is_active = 1
        
        try:
            save_one_user(new_user)
            user = UserLogin(
                id=new_user.name,
                name=new_user.name,
                user_type=new_user.user_type,
                is_ban=new_user.is_ban,
                created_at=new_user.created_at,
                last_login=new_user.last_login
            )
            login_user(user)
            flash("注册成功并已登录", "success")
            return redirect(url_for("/.index"))
        except Exception as e:
            flash(f"注册失败: {str(e)}", "error")
            return render_template("login.html", r_txt="注 册")
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
