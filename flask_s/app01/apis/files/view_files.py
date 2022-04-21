from flask import Blueprint, request, jsonify, current_app, g, send_file, render_template
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
    data_saves.save_data(datas, 1, 'files')
    x = core.get_files(os.y.up_files_path)
    x2 = list(zip(list(x), [str(i) for i in x]))
    return render_template('down.html', navigation=x)


@bp.route('/<string:file_name>', methods=('GET',))
def down(file_name):
    datas = Dict({
        'data': Dict() | request.args | request.form,
        'laizi': request.args.get('laizi') or request.form.get('laizi'),
        'time': time.strftime("%Y-%m-%d %X"),
        'ip': request.headers.get('X-Forwarded-For', request.remote_addr),
        'who': 'files'
    })
    data_saves.save_data(datas, 1, 'files/down')
    x = os.path.join(os.y.up_files_path, file_name)
    if os.path.isfile(x):
        return send_file(x)
    return jsonify({'msg': '文件不存在'})


@bp.route(rule='/up', methods=('GET', 'POST'))
def up_file():
    datas = Dict({
        'data': Dict() | request.args | request.form,
        'laizi': request.args.get('laizi') or request.form.get('laizi'),
        'time': time.strftime("%Y-%m-%d %X"),
        'ip': request.headers.get('X-Forwarded-For', request.remote_addr),
        'who': 'files'
    })
    data_saves.save_data(datas, 1, 'files/up')
    if request.method == "GET":
        date1 = time.strftime("%d%H")
        return render_template('up_file.html')

    if request.method == 'POST':
        file = request.files.get('file')
        file_name = file.filename
        myfuncs.save_file(request.files.get('file'),
                          os.path.join(os.y.up_files_path, file_name))
        # return jsonify({"msg": "ok"})
        return render_template('down_ok.html')
