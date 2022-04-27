
from flask import Blueprint, redirect, request, g, render_template
from entities import data_saves
from .. import myfuncs
import time

service_name = '/'
bp = Blueprint(service_name, __name__)


@bp.route('/', methods=['GET'])
def index():
    data = myfuncs.get_datas(request)
    data_saves.save_data(data, 1, 'gen')
    return '你好，这里是根节点，你为什么会来这里呢？我很好奇，你不该来这个网站的'

@bp.route('/robot.txt', methods=['GET'])
def robot():
    data = myfuncs.get_datas(request)
    data_saves.save_data(data, 1, 'robot')
    return 'User-agent: *\nDisallow: /'


@bp.route('/md', methods=['GET'])
def md():
    data = myfuncs.get_datas(request)
    data_saves.save_data(data, 1, 'gen')
    return data


@bp.route('/emi/', methods=['GET', 'POST'])
def emi():
    # 带着arg和postdata跳转到email模块
    # print(app.config)
    return redirect('/email/', request.base_url)
