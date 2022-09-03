from flask import Blueprint, request, jsonify, current_app, g, send_file, render_template
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

service_name = 'to_v'

bp = Blueprint(service_name, __name__, url_prefix=f'/{service_name}')
data_path = './app01/apis/to_video/y_config.json'     # 这个东西的数据目录

def load_json():
    with open(data_path, 'r') as f:
        z = f.read()
        if not z:
            return Dict({})
        return Dict(json.loads(z))

def save_json(data):
    with open(data_path, 'w') as f:
        json.dump(data, f, indent=4)

@bp.route('/', methods=('GET', 'POST'))
def index():
    """
    

    """
    x = request.args.get('x') or request.form.get('x')
    
    jqm = jiqima = request.args.get('mqj') or request.form.get('mqj')  # 机器码
    # 如果json存在
    ip = request.args.get('ip') or request.form.get('ip')
    if not ip:
        return jsonify({"code": -1, "msg": "ip不能为空"})
    video_data = Dict({
    "v1": [0, 'http://{ip}:30080/D%3A/FFOutput/v1.mp4'],
    "v2": [0, 'http://{ip}:30080/D%3A/FFOutput/v2.mp4'],
    "v3": [0, 'http://{ip}:30080/D%3A/FFOutput/v3.mp4'],
    "v4": [0, 'http://{ip}:30080/D%3A/FFOutput/v4.mp4'],
    })
    if not os.path.exists(data_path):
        save_json(video_data.to_dict())
        

    video_data = load_json() or video_data
    
    if x not in video_data:
        return jsonify({"code": -1, "msg": "x参数错误"})
    
    if video_data[x][0] > 0:
        return jsonify({"code": -1, "msg": "视频已经播放完毕"})
    video_data[x][0] += 1
    save_json(video_data)
    print(video_data[x][1].format(ip=ip))
    return jsonify({"code": 0, "data": video_data[x][1].format(ip=ip)})
