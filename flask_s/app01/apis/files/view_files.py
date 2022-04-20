from flask import Blueprint, request, jsonify, current_app, g, send_file
from app01 import myfuncs
from addict import Dict
from utils import send_email
from datetime import datetime
import time
import os
from entities import data_saves
from utils import core

service_name = 'files'

bp = Blueprint(service_name, __name__, url_prefix='/files')

# /files/


@bp.route('/', methods=('GET', 'POST'))
def index():
    datas = Dict({
        'data': Dict() | request.args | request.form,
        'laizi': request.args.get('laizi') or request.form.get('laizi'),
        'time': time.strftime("%Y-%m-%d %X"),
        'ip': request.headers.get('X-Forwarded-For', request.remote_addr),
        'who': 'files'
    })
    x = core.get_files(os.y.up_files_path)
    return jsonify(x)


@bp.route('/<string:file_name>', methods=('GET',))
def down(file_name):
    x = os.path.join(os.y.up_files_path, file_name)
    if os.path.isfile(x):
        return send_file(x)
    return jsonify({'msg': 'file not found'})


@bp.route(rule='/up', methods=('GET', 'POST'))
def up_file():
    if request.method == "GET":
        return send_file(os.path.join(os.y.root_path1, 'static', 'up_file.html'))

    if request.method == 'POST':
        file = request.files.get('file')
        file_name = file.filename
        myfuncs.save_file(request.files.get('file'), os.path.join(os.y.up_files_path, file_name))
        # 将文件信息保存到数据库
        return jsonify({"msg": "ok"})
