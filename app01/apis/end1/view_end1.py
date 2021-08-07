
from flask import Blueprint,request,jsonify,current_app

service_name = 'end1'
bp = Blueprint(service_name, __name__)

# /end1/
@bp.route('/', methods=('GET','POST'))
def index():
    """
    1.拿到header中的参数，判断
    2. 将ip地址写入数据

    """
    header = request.headers
    if header.get('is_y') not in [1, '1']:
        return 'hello,'

    who = header.get('who')
    # 拿取ip地址
    ip = request.remote_addr
    # 写入数据库
    print(f'拿到ip了，ip是{ip}')

