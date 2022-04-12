from flask import Blueprint,request,jsonify,current_app,g
from app01 import myfuncs
from addict import Dict
from utils import send_email
from datetime import datetime
import time
import threading

service_name = 'email'

# 同时接受/emi和/email两种url前缀
bp = Blueprint(service_name, __name__, url_prefix='/email')



# /email/
@bp.route('/', methods=('GET','POST'))
def index():
    # 获取请求参数
    datas = Dict()
    args1 = request.args
    post_data = request.form
    datas.update(args1)
    datas.update(post_data)
    nowtime = time.strftime("%Y-%m-%d %X")
    laizi = args1.get('laizi') or post_data.get('laizi')
    # 异步发送邮件
    threading.Thread(target=send_email.send_email, args=([f"来自{laizi}",f"data: {datas}", nowtime],)).start()
    # TODO 回头添加入库

    return {'laizi':laizi,'data':datas,'nowtime':nowtime}
