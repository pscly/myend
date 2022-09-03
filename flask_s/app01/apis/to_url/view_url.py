from flask import Blueprint, request, jsonify, current_app, g, send_file, render_template, redirect
from app01 import myfuncs
from addict import Dict
from utils import send_email
from datetime import datetime
import time
import os
import json
from entities import data_saves
from utils import core
from entities.mymongo import MyMongo1

service_name = 'to_url'

bp = Blueprint(service_name, __name__, url_prefix=f'/{service_name}')

data_path = './app01/apis/to_url/y_urls.json'     # 这个东西的数据目录

def load_json(path=data_path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return Dict({})
    with open(path, 'r') as f:
        z = f.read()
        return Dict(json.loads(z))

def save_json(data, path=data_path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

@bp.route('/', methods=('GET', 'POST'))
def index():
    """
    

    """
    error_url = 'https://www.4399.com/'
    
    x = request.args.get('x') or request.form.get('x')
    if not x:
        return jsonify({"code": -1, "msg": "x?"})
    
    urls_data = Dict(load_json(data_path)) or Dict({
        'pscly': [1, 'https://y.pscly.cn'],
        'baidu': [1, 'https://baidu.com'],
        })  # {'a1': 'http://baidu.com/', 'b1': 'http://google.com/'}


    if x not in urls_data:
        return jsonify({"code": -1, "msg": "x!"})
    
    if urls_data[x][0] < 1:
        if error_url:
            return redirect(error_url)
        return jsonify({"code": -1, "msg": "error"})
    urls_data[x][0] -= 1
    urls_data.open = urls_data.open or 0
    urls_data.open += 1
    save_json(urls_data, data_path)
    return redirect(urls_data[x][1])

