from flask import Flask, Blueprint
import yaml
import os
import json
from addict import Dict
from pathlib import Path
from flask_login import LoginManager, UserMixin

from app01.route import routers
from utils.login1 import User, get_all_users
from utils.webpy import WebFunc


def load_conf(mode: str, conf_name: str = "config.yaml"):
    """
    读取conf，
    mode: 是什么环境， 开发还是生产(DEVELOPMENT, PRODUCTION)
    conf_nae: 配置文件名
    """
    with open(f"configs/{conf_name}", encoding="utf-8") as f:
        conf = yaml.safe_load(f)

    return conf[mode.upper()]


def load_json(path="configs/y_data.json"):
    js_path = Path(path)
    if (not js_path.exists()) or (os.path.getsize(path) < 3):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(Dict({}), f)
    with open(path, "r", encoding="utf-8") as f:
        return Dict(json.load(f))


def save_json(data, path="configs/y_data.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def create_app():
    app = Flask(
        "app",
        template_folder=os.path.join("static", "jinja_templates"),
        static_folder="static",
        static_url_path="/static",
    )
    mode = os.environ.get("MODE", "DEVELOPMENT")
    conf = load_conf(mode)
    app.config.update(conf)
    # 静态资源文件夹为 static和files
    os.y.root_path1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.y.up_files_path = os.path.join(os.y.root_path1, "static", "up_files")
    os.y.config = conf
    os.y.ydata = load_json()
    os.y.app = app
    os.y.y = []  # 用于验证判断
    static_folder = os.path.join(os.y.root_path1, "static")
    os.y.static_folder = static_folder
    app.secret_key = "y_yend_001"

    # 注册api  # 其实可以街道方法中
    for router in routers:
        if isinstance(router, Blueprint):
            app.register_blueprint(router)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(name):
        # 数据库
        users = get_all_users()
        if name not in users:
            return
        user = User()
        user.id = name
        return user

    @login_manager.request_loader
    def request_loader(request):
        users = get_all_users()
        name = request.form.get("name")
        if name not in users:
            return
        user = User()
        user.id = name
        return user

    # 注册过滤器
    WebFunc(app)
    return app
