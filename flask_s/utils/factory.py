import os

import yaml
from addict import Dict
from app01.route import routers
from flask import Blueprint, Flask


def load_conf(mode: str, conf_name: str = 'config.yaml'):
    """
    读取conf，
    mode: 是什么环境， 开发还是生产(DEVELOPMENT, PRODUCTION)
    conf_nae: 配置文件名
    """
    with open(f"configs/{conf_name}", encoding='utf-8') as f:
        conf = yaml.safe_load(f)

    return conf[mode.upper()]


def create_app():
    app = Flask('app', template_folder=os.path.join(
        'static', 'jinja_templates'), static_folder='static', static_url_path='/static')
    mode = os.environ.get('MODE', "DEVELOPMENT")
    conf = load_conf(mode)
    app.config.update(conf)
    app.config = Dict(app.config)
    # app.y = Dict({'a': 1})
    # 静态资源文件夹为 static和files
    os.y.root_path1 = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    os.y.up_files_path = os.path.join(os.y.root_path1, 'static', 'up_files')
    static_folder = os.path.join(os.y.root_path1, 'static')

    # 注册api  # 其实可以街道方法中
    for router in routers:
        if isinstance(router, Blueprint):
            app.register_blueprint(router)

    return app
