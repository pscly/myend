from flask import Flask, Blueprint, g
import yaml
import os
import json
from addict import Dict
from pathlib import Path
from flask_login import LoginManager, UserMixin

from app01.route import routers
from utils.webpy import WebFunc

from pyaml_env import parse_config
from entities.mypgsql import YSqlTool
from entities.models import Users
from utils.database import get_db

# 新增：导入必要的模块
from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import inspect
from utils.extensions import init_extensions



def load_conf(mode: str, conf_name: str = "configs/config.yaml"):
    """
    读取conf，
    mode: 是什么环境， 开发还是生产(DEVELOPMENT, PRODUCTION)
    conf_nae: 配置文件名
    """
    print(f'使用的是 {mode} 环境', )
    # with open(f"configs/{conf_name}", encoding="utf-8") as f:
    #     conf = yaml.safe_load(f)
    conf = parse_config(f"{conf_name}")
    # save_json(conf[mode.upper()], 'configs/x.json')
    return conf[mode.upper()]


def load_json(path="configs/config.json"):
    js_path = Path(path)
    if (not js_path.exists()) or (os.path.getsize(path) < 3):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(Dict({}), f)
    with open(path, "r", encoding="utf-8") as f:
        return Dict(json.load(f))


def save_json(data, path="configs/config.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def check_and_apply_migrations(app):
    """检查并应用数据库迁移"""
    alembic_cfg = Config("alembic.ini")
    script = ScriptDirectory.from_config(alembic_cfg)

    with app.app_context():
        # 获取数据库连接
        engine = get_db().engine

        def get_current_revision(connection):
            context = MigrationContext.configure(connection)
            return context.get_current_revision()

        with engine.connect() as connection:
            current_rev = get_current_revision(connection)

        # 获取最新的迁移版本
        head_rev = script.get_current_head()

        print(f"数据库的版本: {current_rev}")    # 意思是 
        print(f"迁移脚本的版本: {head_rev}")

        if current_rev is None and head_rev is None:
            print("数据库和迁移脚本都是空的。正在创建初始迁移...")
            # 创建初始迁移
            command.revision(alembic_cfg, autogenerate=True, message="init db")
            command.upgrade(alembic_cfg, "head")
            head_rev = script.get_current_head()
            print(f"创建了初始迁移: {head_rev}")

        if current_rev != head_rev:
            print("检测到数据库需要更新，正在应用迁移...")
            command.revision(alembic_cfg, autogenerate=True, message="update db")
            command.upgrade(alembic_cfg, "head")
            print("数据库迁移完成。")
        else:
            print("数据库已是最新版本。")


def create_app():
    app = Flask(
        "app",
        template_folder=os.path.join("static", "jinja_templates"),
        static_folder="static",
        static_url_path="/static",
    )
    mode = os.environ.get("MODE", "production")
    conf = load_conf(mode, "configs/config.yaml")  #读取的是yaml configs/config.
    conf.update(os.y.data2)
    app.config.update(conf)

    # 初始化数据库连接
    with app.app_context():
        db = get_db()
        app.db = db

    # 设置 Alembic 配置
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", app.config['SQLALCHEMY_DATABASE_URI'])

    # 新增：检查并应用数据库迁移
    check_and_apply_migrations(app)

    # 静态资源文件夹为 static和files
    os.y.root_path1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.y.up_files_path = os.path.join(os.y.root_path1, "static", "up_files")
    os.y.config = conf
    # os.y.ydata = load_json()
    os.y.app = app
    os.y.y = []  # 用于验证判断
    static_folder = os.path.join(os.y.root_path1, "static")
    os.y.static_folder = static_folder
    app.secret_key = "y_yend_001"

    # 注册api  # 其实可以街道方法中
    for router in routers:
        if isinstance(router, Blueprint):
            app.register_blueprint(router)


    # 登录的地方
    # login_manager = LoginManager()
    # login_manager.init_app(app)
    init_extensions(app)        # 例如判断是否登录的地方

    WebFunc(app)

    # 注册数据库关闭函数
    @app.teardown_appcontext
    def close_db(error):
        if hasattr(g, 'db'):
            g.db.close()

    return app
