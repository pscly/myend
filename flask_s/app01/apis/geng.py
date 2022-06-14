
from flask import Blueprint, redirect, request, g, render_template, render_template
from entities import data_saves
from .. import myfuncs
import time
import random

service_name = '/'
bp = Blueprint(service_name, __name__)


@bp.route('/', methods=['GET'])
def index():
    data = myfuncs.get_datas(request)
    data_saves.save_data(data, 1, 'gen')
    yyids = [
        28188427,
        1407112865,
        1919147134,
        1453957944,
        1886371886,
        450853439
    ]
    return render_template('geng.html', yyid=random.choice(yyids), imgid=str(random.randint(1, 18)))
    # return render_template('down.html', files=files, imgid=str(random.randint(1, 18)))
    # return render_template('down.html', datas={"files": files, "imgid": random.randint(1, 18)})


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
