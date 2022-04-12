
from flask import Blueprint, redirect, request, g

service_name = '/'
bp = Blueprint(service_name, __name__)


# /
@bp.route('/', methods=['GET'])
def index():
    # TODO 回头添加入库
    return '你好，这里是根节点，你为什么会来这里呢？我很好奇，你不该来这个网站的'

# /robot.txt
@bp.route('/robot.txt', methods=['GET'])
def robot():
    return 'User-agent: *\nDisallow: /'


@bp.route('/md', methods=['GET'])
def md():
    # TODO 回头添加入库
    ip = request.remote_addr
    hostname = request.host
    
    return {
        'ip': ip,
        'hostname': hostname,
        'e_wy': 'UXQSTCRIEKULJEDL',
    }

# /emi/*
@bp.route('/emi/', methods=['GET', 'POST'])
def emi():
    # 带着arg和postdata跳转到email模块
    # print(app.config)
    return redirect('/email/', request.base_url)

