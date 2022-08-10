from flask import Blueprint, request, jsonify, current_app, g, send_file, render_template
from app01 import myfuncs
from addict import Dict
from utils import send_email
from datetime import datetime
import time
import json
import os
from entities import data_saves
from utils import core
from entities.mymongo import MyMongo1

service_name = 'datas'

bp = Blueprint(service_name, __name__, url_prefix=f'/{service_name}')



@bp.route('/up', methods=('GET', 'POST'))
def index():
    """
    验证功能
    拿到 key 
        用 key 去数据库比对,
        用 key 的头部[]去比对, 如果头部不匹配，那就直接返回错误(可以放到c端)
        数据库中拿到 key， 查看是否当前时间, 
            sjk = 100
            now = 80
            
    参数:
        j1: json_data
        zhu: 要么j1里面带
    """
    mo = MyMongo1('datas')
    text = request.args.get('j1') or request.form.get('j1') or ''
    text.strip()
    if not text:
        return jsonify({'msg': 'j1 错误，缺少参数'})
    try:
        data1 = json.loads(text)
    except Exception as e:
        return jsonify({'msg': 'j1 错误，不是json格式'})
    if not data1.get('zhu'):
        return jsonify({'msg': 'j1 错误，缺少参数 zhu'})
    data = Dict(data1)
    # 连接 mongo 数据库
    zhu = data.zhu
    user = Dict(mo.find({'zhu': zhu}))
    if user:
        user.update(data)
    else:
        user = data
    mo.save(user)
    
    mo2 = MyMongo1('datas_zhu')
    user2 = Dict(mo2.find({'zhu': zhu}))
    if user2:
        user2.time = time.strftime("%Y-%m-%d %X")
    else:
        user2 = Dict({'zhu': zhu, 'time': time.strftime("%Y-%m-%d %X")})
    mo2.save(user2)
    return jsonify({'code': 1, 'msg': 'ok'})

@bp.route('/down2', methods=('GET', 'POST'))
def down2():
    mo2 = MyMongo1('datas_zhu')
    users = mo2.find_all() 
    data = [Dict(i).to_dict() for i in users]
    for i in data:
        i.pop('_id')
    # 将字典按照时间排序
    data.sort(key=lambda x: x['time'], reverse=True)
    return jsonify({'code': 1, 'msg': 'ok', 'data': data})

@bp.route('/down1', methods=('GET', 'POST'))
def down1():
    """ 
    """
    mo = MyMongo1('datas')
    y = request.args.get('y') or request.form.get('y') or ''
    zhu = request.args.get('zhu') or request.form.get('zhu')
    if time.strftime("%d%H") != y:
        return jsonify({'msg': '错误, 此页面暂时不允许访问, 服务器内部错误'})
    if zhu:
        data = mo.find({'zhu': zhu})
        data = Dict(data)
        data.pop('_id')
    else:
        data = mo.find_all()
        data = [Dict(i) for i in data]
        for i in data:
            i.pop('_id')
    return jsonify({'code': 1, 'msg': 'ok', 'data': data})


# @bp.route('/login', methods=('GET', 'POST'))
# def login():
    # user = request.args.get('user') or request.form.get('user') or ''
    # pwd = request.args.get('pwd') or request.form.get('pwd') or ''
    
    