
from flask import Blueprint, redirect, request, g, render_template
from entities import data_saves
import time

service_name = '/'
bp = Blueprint(service_name, __name__)


@bp.route('/', methods=['GET'])
def index():
    data = {
        'time': time.strftime("%Y-%m-%d %X"),
        'ip': request.headers.get('X-Forwarded-For', request.remote_addr),
    }
    data_saves.save_data(data, 1, 'gen')
    return '你好，这里是根节点，你为什么会来这里呢？我很好奇，你不该来这个网站的'

@bp.route('/robot.txt', methods=['GET'])
def robot():
    data = {
        'time': time.strftime("%Y-%m-%d %X"),
        'ip': request.headers.get('X-Forwarded-For', request.remote_addr),
    }
    data_saves.save_data(data, 1, 'robot')
    return 'User-agent: *\nDisallow: /'


@bp.route('/md', methods=['GET'])
def md():
    data = {
        'time': time.strftime("%Y-%m-%d %X"),
        'ip': request.headers.get('X-Forwarded-For', request.headers.get('X-Forwarded-For', request.remote_addr)),
        'hostname': request.host
    }
    data_saves.save_data(data, 1, 'gen')
    return data


@bp.route('/emi/', methods=['GET', 'POST'])
def emi():
    # 带着arg和postdata跳转到email模块
    # print(app.config)
    return redirect('/email/', request.base_url)
