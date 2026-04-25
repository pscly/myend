from flask import Blueprint, request, jsonify, current_app, g, send_file, render_template, redirect
from app01 import myfuncs
from addict import Dict
from utils import send_email
from datetime import datetime
import time
import os
from entities import data_saves
from utils import core
from flask_login import current_user

service_name = 'files2'

bp = Blueprint(service_name, __name__, url_prefix=f'/{service_name}')


def get_files2_pwd():
    return str(os.y.config.get('FILES2_PWD') or 'y')


def check_files2_pwd():
    return request.values.get('pwd') == get_files2_pwd()


def is_files2_allowed():
    return current_user.is_authenticated or check_files2_pwd()


def should_require_pwd_input():
    return not current_user.is_authenticated


def redirect_to_files():
    return redirect('/files')


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
    return 0  # assume small enough


@bp.route('/', methods=('GET', 'POST'))
def index():
    if not is_files2_allowed():
        return redirect_to_files()
    datas = myfuncs.get_datas(request)
    data_saves.save_data(datas, 1, service_name)
    files = core.get_files(f'{os.y.up_files_path}2')
    return render_template(
        'down.html',
        files=files,
        require_pwd=should_require_pwd_input(),
        pwd=request.values.get('pwd', ''),
    )


@bp.route('/<string:file_name>', methods=('GET',))
def down(file_name):
    if not is_files2_allowed():
        return redirect_to_files()
    datas = myfuncs.get_datas(request)
    data_saves.save_data(datas, 1, f'{service_name}/down')
    x = os.path.join(f'{os.y.up_files_path}2', file_name)
    if os.path.isfile(x):
        return send_file(x)
    return jsonify({'msg': '文件不存在'})


@bp.route(rule='/up', methods=('GET', 'POST'))
def up_file():
    datas = myfuncs.get_datas(request)
    data_saves.save_data(datas, 1, f'{service_name}/up')
    if request.method == "GET":
        return render_template(
            'up_file.html',
            require_pwd=should_require_pwd_input(),
            pwd=request.values.get('pwd', ''),
        )

    if request.method == 'POST':
        require_pwd = should_require_pwd_input()
        if not is_files2_allowed():
            return render_template(
                'up_file.html',
                require_pwd=require_pwd,
                pwd=request.values.get('pwd', ''),
                error_msg='密码错误，文件未上传',
            )
        file = request.files.get('file')
        # 如果文件大小超过300mb, 则返回错误

        file_name = request.form.get('file_name') or file.filename
        myfuncs.save_file(request.files.get('file'),
                          os.path.join(f'{os.y.up_files_path}2', file_name))
        return render_template('down_ok.html')
