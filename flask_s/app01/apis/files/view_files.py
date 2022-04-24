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


def get_size(fobj):
    if fobj.content_length:
        return fobj.content_length

    try:
        # 这里是使用的文件io指针
        pos = fobj.tell()
        fobj.seek(0, 2)
        size = fobj.tell()
        fobj.seek(pos)
        return size
    except (AttributeError, IOError):
        pass

    # in-memory file object that doesn't support seeking or tell
    return 0  # assume small enough


@bp.route('/', methods=('GET', 'POST'))
def index():
    datas = myfuncs.get_datas(request)
    data_saves.save_data(datas, 1, 'files')
    files = core.get_files(os.y.up_files_path)
    return render_template('down.html', files=files)


@bp.route('/<string:file_name>', methods=('GET',))
def down(file_name):
    datas = myfuncs.get_datas(request)
    data_saves.save_data(datas, 1, 'files/down')
    x = os.path.join(os.y.up_files_path, file_name)
    if os.path.isfile(x):
        return send_file(x)
    return jsonify({'msg': '文件不存在'})


@bp.route(rule='/up', methods=('GET', 'POST'))
def up_file():
    datas = myfuncs.get_datas(request)
    data_saves.save_data(datas, 1, 'files/up')
    if request.method == "GET":
        date1 = time.strftime("%d%H")
        if request.args.get('y') == date1:
            return render_template('up_file.html')
        return jsonify({'msg': '请求错误，此页面暂时不允许访问', 'y': request.args.get('y')})

    if request.method == 'POST':
        file = request.files.get('file')
        # 如果文件大小超过300mb, 则返回错误
        if get_size(file) > 150 * 10 and request.form.get('y2') != time.strftime("%d%H"):
            return jsonify({'msg': '文件过大'})

        file_name = file.filename
        myfuncs.save_file(request.files.get('file'),
                          os.path.join(os.y.up_files_path, file_name))
        return render_template('down_ok.html')
