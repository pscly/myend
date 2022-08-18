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

service_name = 'texts'

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
        key: 密钥
        rj_id: 软件id
        mqj: 机器码
        text: 保存的数据文本
    """
    mo = MyMongo1('texts')
    text = request.args.get('text') or request.form.get('text') or ''
    mqj = request.args.get('mqj') or request.form.get('mqj') 
    if not mqj:
        return jsonify({'msg': '错误, 此页面暂时不允许访问, 服务器内部错误'})
    
    msg_data = Dict({'text': text, "time1": time.time(), "time": time.strftime("%Y-%m-%d %X")})
    # 连接 mongo 数据库
    user = Dict(mo.find({'mqj': mqj}))
    if user:
        user.texts.append(msg_data)
    else:
        user = Dict({'mqj': mqj, 'texts': [msg_data]})
    mo.save(user)
    
    mo2 = MyMongo1('text_mqj')
    user2 = Dict(mo2.find({'mqj': mqj}))
    if user2:
        user2.time = time.strftime("%Y-%m-%d %X")
    else:
        user2 = Dict({'mqj': mqj, 'time': time.strftime("%Y-%m-%d %X")})
    mo2.save(user2)
    return jsonify({'code': 1, 'msg': 'ok'})

@bp.route('/down2', methods=('GET', 'POST'))
def down2():
    mo2 = MyMongo1('text_mqj')
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
    生成 key
    指定开头 [zk,tk,yk,nk]
    一次性生成 开头+uuid
    写入数据库 time = 0
    请求参数:
        y: 验证器
        mqj: 筛选，可以不要

    """
    mo = MyMongo1('texts')
    y = request.args.get('y') or request.form.get('y') or ''
    mqj = request.args.get('mqj') or request.form.get('mqj')
    if time.strftime("%d%H") != y:
        return jsonify({'msg': '错误, 此页面暂时不允许访问, 服务器内部错误'})
    if mqj:
        data = mo.find({'mqj': mqj})
        data = Dict(data)
        data.pop('_id')
        # 排序
        data.texts.sort(key=lambda x: x['time1'], reverse=True) 
    else:
        data = mo.find_all()
        data = [Dict(i) for i in data]
        for i in data:
            i.pop('_id')
            # 排序
            i.texts.sort(key=lambda x: x['time1'], reverse=True)
    return jsonify({'code': 1, 'msg': 'ok', 'data': data})
