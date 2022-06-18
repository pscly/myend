from flask import Blueprint, request, jsonify, current_app, g, send_file, render_template
from app01 import myfuncs
from addict import Dict
from utils import send_email
from datetime import datetime
import time
import os
from entities import data_saves
from utils import core
from entities.mymongo import MyMongo1

service_name = 'rum'

bp = Blueprint(service_name, __name__, url_prefix='/rum')

ka_list = ['zk', 'tk', 'yk', 'nk']


@bp.route('/jihuo', methods=('GET', 'POST'))
def index():
    """
    验证功能
    拿到 key 
        用 key 去数据库比对,
        用 key 的头部[]去比对, 如果头部不匹配，那就直接返回错误(可以放到c端)
        数据库中拿到 key， 查看是否当前时间, 
            sjk = 100
            now = 80
    """
    key = request.args.get('key') or request.form.get('key')
    if key[:2] not in ka_list:
        return jsonify({"code": -1, "msg": "激活码错误"})
    jiqima = request.args.get('mqj') or request.form.get('mqj')  # 机器码
    if not jiqima:
        return jsonify({"code": -1, "msg": "激活码错误."})
    mo = MyMongo1('key')
    if key_data := mo.find({'key': key}):
        mo.update({'key': key_data['key']}, {
                  'endtime': time.strftime("%Y-%m-%d %X")})
        key_data = Dict(key_data)
        if key_data['time'] > time.time():
            if key_data['jiqima'] != jiqima:
                jf = 1
                mo.update({'key': key_data['key']}, {
                    'time': key_data['time'] - (60 * 60 * 24 * jf), 'jiqima': jiqima, 'jiqimas': key_data['jiqimas'] + [jiqima]})
                return jsonify({"code": 1, "msg": f"解绑成功，激活码时间减少{jf}天, 当前剩余时间: {round(int(key_data['time'] - time.time()) / 60 / 60 / 24,2) -1 }天", 'time': key_data['time']})
            return jsonify({"code": 1, "msg": f"剩余时间: {round(int(key_data['time'] - time.time()) / 60 / 60 / 24,2)}天", 'time': key_data['time']})
        elif key_data['time'] == 0:
            if key[:2] == 'zk':
                # 周卡
                key_data.time = time.time() + 60 * 60 * 24 * 7
            elif key[:2] == 'tk':
                # 天卡
                key_data.time = time.time() + 60 * 60 * 24
            elif key[:2] == 'yk':
                # 月卡
                key_data.time = time.time() + 60 * 60 * 24 * 31
            elif key[:2] == 'nk':
                # 年卡
                key_data.time = time.time() + 60 * 60 * 24 * 365
            else:
                return jsonify({"code": -1, "msg": "key error"})
            key_data.jiqima = jiqima
            key_data.jiqimas = [jiqima]
            mo.update({'key': key}, key_data)
            return jsonify({"code": 1, 'msg': f"剩余时间: {round(int(key_data['time'] - time.time()) / 60 / 60 / 24,2)}天", 'time': key_data['time']})
        else:
            return jsonify({"code": -1, "msg": "激活码过期"})

    return jsonify({"code": -1, "msg": "激活码错误"})


@bp.route('/addkey', methods=('GET', 'POST'))
def addkey():
    """ 
    生成 key
    指定开头 [zk,tk,yk,nk]
    一次性生成 开头+uuid
    写入数据库 time = 0
    """
    y = request.args.get('y')
    if y != time.strftime("%d%H"):
        return jsonify({'msg': '错误, 此页面暂时不允许访问, 服务器内部错误'})
    key = request.args.get('key')

    if key not in ka_list:
        return jsonify({'msg': '错误, 此页面暂时不允许访问, 服务器内部错误'})
    k_num = request.args.get('num')
    head = request.args.get('head')
    if not head:
        return jsonify({'msg': '错误,缺失创建者'})
    # 将head的每个字符 +1
    key_num = 20
    if k_num.isdigit() and int(k_num) > 0:
        key_num = int(k_num)
    key_list = [{'key': f'{key}{core.get_ran_str(24)}',
                 'time': 0,
                 'create_time': time.strftime("%Y-%m-%d %H:%M:%S"),
                 'user': head}
                for i in range(key_num)]
    key_list1 = [i['key'] for i in key_list]
    mo = MyMongo1('key')
    mo.save(key_list)
    return jsonify({'msg': 'ok', 'key_list': key_list1})


@bp.route('/getkey', methods=('GET', 'POST'))
def getkey():
    y = request.args.get('y') or request.form.get('y')
    if y != time.strftime("%d%H"):
        return jsonify({'msg': '错误, 此页面暂时不允许访问, 服务器内部错误'})
    gq = request.args.get('gq') or request.form.get('gq') or 0  # 是否要看过期的
    mo = MyMongo1('key')
    # 查询 time = 0 和 time > time.time()
    x = mo.find_many({})
    if gq == '1':
        x1 = [{
            '类型': '未使用的',
            'key': i['key'],
            'time': i['time'],
            'create_time': i['create_time'],
            'endtime': i.get('endtime'),
            '机器码s': i.get('jiqimas'),
        } for i in x if i['time'] == 0]
    elif gq == '2':
        x1 = [{
            '类型': '全部',
            'key': i['key'],
            'time': i['time'],
            'create_time': i['create_time'],
            'endtime': i.get('endtime'),
            '机器码s': i.get('jiqimas'),
        } for i in x]
    elif gq == '3':
        x1 = [{
            '类型': '使用中的',
            'key': i['key'],
            'time': i['time'] - time.time(),
            'create_time': i['create_time'],
            'endtime': i.get('endtime'),
            '机器码s': i.get('jiqimas', []),
        } for i in x if i['time'] > time.time()]
    else:
        x1 = []
    return jsonify({'msg': 'ok', 'key_list': x1})
