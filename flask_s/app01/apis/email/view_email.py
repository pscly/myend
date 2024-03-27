from flask import Blueprint, request, jsonify, current_app, g
from app01 import myfuncs
from addict import Dict
from utils import send_email
from datetime import datetime
import time
from entities import data_saves

service_name = 'ime'

bp = Blueprint(service_name, __name__, url_prefix='/ime')


@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.args | request.form:
        datas = myfuncs.get_datas(request)
        if request.args.get('addr'):
            email_addr= request.args.get('addr')
            data_saves.save_data(datas, 2, 'email', email_addr=email_addr)
        else:
            data_saves.save_data(datas, 2, 'email')
        return datas
    return """何不去看看 v2 呢? (域名/ime/v2/?msg=xxx&addr=xxx@qq.com)"""

@bp.route('v2/', methods=('GET', 'POST'))
def index2():
    """
    这个就是发送纯文本
    只会接受一个参数, msg
    """
    datas =  Dict() | request.args | request.form,
    if datas:
        if request.args.get('msg'):
            datas = request.args.get('msg')
        if request.args.get('addr'):
            email_addr= request.args.get('addr')
            data_saves.save_data(datas, 2, 'email', email_addr=email_addr)
        else:
            data_saves.save_data(datas, 2, 'email')
        return datas
    return '''http://127.0.0.1:31001/ime/2/?msg=xxx&addr=xxx@qq.com'''
