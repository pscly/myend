from flask import Flask
import yaml
import os


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

    # 注册api
    from app01.route import router
    from app01.apis.router.routers import routers
    register_api(app, routers)

    return app

