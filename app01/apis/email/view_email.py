
from flask import Blueprint,request,jsonify,current_app,g
from app01 import myfuncs
from datetime import datetime

service_name = 'email'

# 同时接受/emi和/email两种url前缀
bp = Blueprint(service_name, __name__, url_prefix='/email')



# /email/
@bp.route('/', methods=('GET','POST'))
def index():
    # 获取请求参数
    args1 = request.args
    post_data = request.form
    print(args1)
    
    return {'args1':args1,'post_data':post_data}
