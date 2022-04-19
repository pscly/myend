from flask import Blueprint, request, jsonify, current_app, g
from app01 import myfuncs
from addict import Dict
from utils import send_email
from datetime import datetime
import time
from entities import data_saves

service_name = 'email'

bp = Blueprint(service_name, __name__, url_prefix='/email')

# /email/


@bp.route('/', methods=('GET', 'POST'))
def index():
    datas = Dict({
        'data': Dict() | request.args | request.form,
        'laizi': request.args.get('laizi') or request.form.get('laizi'),
        'time': time.strftime("%Y-%m-%d %X"),
        'ip': request.headers.get('X-Forwarded-For', request.remote_addr),
        'who': 'email'
    })
    data_saves.save_data(datas, 2, 'email')
    return datas
