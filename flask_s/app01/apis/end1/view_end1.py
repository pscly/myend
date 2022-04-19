
from flask import Blueprint, request, jsonify, current_app, g
from app01 import myfuncs
from datetime import datetime
from entities import data_saves

service_name = 'end1'
bp = Blueprint(service_name, __name__, url_prefix='/end1')

# /end1/


@bp.route('/', methods=('GET', 'POST'))
def index():
    """
    1.拿到header中的参数，判断
    2. 将ip地址写入数据

    """
    header = request.headers
    base_url = request.base_url
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    data = {
        "is_y": 1,
        "ip": ip,
        "to_url": base_url,
        "who": header.get("who", '匿名'),
    }
    if header.get('is_y') not in [1, '1']:
        data['is_y'] = 0
        print('非1', ip)
        return data

    if request.json:
        data |= request.json

    data['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 写入数据库
    data_saves.save_data(datas, 1, 'end1')

    print(f'拿到ip了，ip是{ip}')
    return data
