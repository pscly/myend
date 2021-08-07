from flask import Flask, Blueprint
import yaml
import os
from app01.route import routers


def load_conf(mode:str, conf_name:str = 'config.yaml'):
    """
    读取conf，
    mode: 是什么环境， 开发还是生产(DEVELOPMENT, PRODUCTION)
    conf_nae: 配置文件名
    """
    with open("configs/{}".format(conf_name)) as f:
        conf = yaml.safe_load(f)

    return conf[mode.upper()]



def create_app():
    app = Flask(__name__)
    mode = os.environ.get('MODE', "DEVELOPMENT")
    conf = load_conf(mode)
    app.config.update(conf)

    # 注册api  # 其实可以街道方法中
    for router in routers:
        if isinstance(router, Blueprint):
            app.register_blueprint(router)

    return app

