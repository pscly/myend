
from flask import Blueprint,request,jsonify,current_app,g
from app01.apis import myfuncs

service_name = 'end1'
bp = Blueprint(service_name, __name__, url_prefix='/end1')

# /end1/
@bp.route('/', methods=('GET','POST'))
def index():
    """
    1.拿到header中的参数，判断
    2. 将ip地址写入数据

    """
    header = request.headers
    base_url = request.base_url
    ip = request.remote_addr
    data = {
        "is_y": 1,
        "send_ip": ip,
        "to_url": base_url,
        "who": header.get("who"),
    }
    for i in header:
        data[i] = header.get(i)

    if header.get('is_y') not in [1, '1']:
        data['is_y'] = 0
        print('非1', ip)
        return data

    # 拿取ip地址
    # 写入数据库
    myfuncs.write_data(data)
    
    print(f'拿到ip了，ip是{ip}')    
    return data

