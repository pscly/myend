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


def get_mo_aut():
    """ 
    从数据库中获取账号
    """
    mo = MyMongo1('aut')
    # 获取 aut 表中 jishu 最低的账号, 并且 ban = 0
    # aut = mo.find({'ban': 0})
    aut_list = mo.find_many({'ban': 0})
    x = 999999
    aut = None
    for aut1 in aut_list:
        if aut1['jishu'] <= x:
            aut = aut1
            x = aut1['jishu']
    # if not aut_list:
    #     return []
    # # 将 jishu 按照 jishu 进行排序
    # for i in aut_list:
    #     print(i['jishu'])
    # if not aut_list:
    #     return []
    # aut = aut_list[0]

    if aut:
        mo.update({'aut': aut.get('aut')}, {'jishu': aut.get('jishu', 0) + 1})
    return aut


def jiqima_db_up(db_data, jiqima):
    """
    数据库中应该保存的格式 [{'机器码': jiqima,'机器码s': ['xx1', 'xx2'], '时间s': ['xxxx-xx-xx xx:xx:xx', 'xxxx-xx-xx xx:xx:xx'], 'end时间': 'xxxx-xx-xx xx:xx:xx'}]'}] 
    """
    # key_data['jiqimas'] + [jiqima]
    old_data = db_data.get('jiqimas')
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(old_data, dict):
        # new_data = {'机器码': jiqima, '机器码s': old_data.get('机器码s').append(
        #     jiqima), '时间s': old_data.get('时间s').append(now_time), 'end时间': now_time}
        # 如果 机器码不是第一次出现, 那就光更新机器码, 然后时间s 增加就行了
        if isinstance(old_data.get('时间s'), list):
            old_data['时间s'] = {jiqima: []}
        if not old_data.get('机器码s'):
            old_data['机器码s'] = []
        if jiqima in old_data.get('机器码s'):
            # 如果这个机器码以前出现过
            if not old_data.get('时间s').get(jiqima):
                old_data.get('时间s')[jiqima] = []
            old_data.get('时间s').get(jiqima).append(now_time)
            new_data = {'机器码': jiqima, '机器码s': old_data.get(
                '机器码s'), '时间s': old_data.get('时间s'), 'end时间': now_time}
        else:
            # 此机器码没有出现过
            old_data.get('时间s')[jiqima] = [now_time]
            old_data.get('机器码s').append(jiqima)
            new_data = {'机器码': jiqima, '机器码s': old_data.get('机器码s'),
                        '时间s': old_data.get('时间s'), 'end时间': now_time}
    else:
        # 是列表, 是老版本
        old_data2 = set(old_data)
        x = list(old_data2)
        x.append(jiqima)
        new_data = {'机器码': jiqima, '机器码s': x,
                    '时间s': {jiqima: [now_time]}, 'end时间': now_time}

    return new_data


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
            
    参数:
        key: 密钥
        rj_id: 软件id
        mqj: 机器码
    """
    key = request.args.get('key') or request.form.get('key')
    rj_id = request.args.get('rj_id') or request.form.get('rj_id') or '' # 软件id
    if (not key) or key[:2] not in ka_list:
        return jsonify({"code": -1, "msg": "激活码错误"})
    jiqima = request.args.get('mqj') or request.form.get('mqj')  # 机器码
    if not jiqima:
        return jsonify({"code": -1, "msg": "激活码错误."})
    mo = MyMongo1('key')
    if key_data := mo.find({'key': key, 'rj_id': rj_id}):
        mo.update({'key': key_data['key']}, {
                  'endtime': time.strftime("%Y-%m-%d %X")})
        key_data = Dict(key_data)
        if key_data['time'] > time.time():
            y_url_db = get_mo_aut()
            y_url = ''
            if y_url_db:
                y_url = get_mo_aut().get('aut')
            if key_data['jiqima'] != jiqima and key_data['jiqima'] != '':   # 如果机器码变动并且不是空
                if key_data.get('jiqima_nojie'):
                    # key_data.jiqima_jie = 1
                    # 可否被解解机器码
                    return jsonify({"code": -1, "msg": "绑定机器码错误"})
            
                jf = 1  # 换机器码扣除几天
                mo.update({'key': key_data['key']}, {
                    # 'time': key_data['time'] - (60 * 60 * 24 * jf), 'jiqima': jiqima, 'jiqimas': key_data['jiqimas'] + [jiqima]})
                    'time': key_data['time'] - (60 * 60 * 24 * jf), 'jiqima': jiqima, 'jiqimas': jiqima_db_up(key_data, jiqima)})
                return jsonify({"code": 1,
                                "msg": f"解绑成功，激活码时间减少{jf}天, 当前剩余时间: {round(int(key_data['time'] - time.time()) / 60 / 60 / 24,2) -1 }天",
                                'time': key_data['time'],
                                'yurl': y_url})

            key_data.jiqima = jiqima
            key_data.jiqimas.append(jiqima)
            return jsonify({"code": 1,
                            "msg": f"剩余时间: {round(int(key_data['time'] - time.time()) / 60 / 60 / 24,2)}天",
                            'time': key_data['time'],
                            'yurl': y_url})
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
            return jsonify({"code": 1,
                            'msg': f"剩余时间: {round(int(key_data['time'] - time.time()) / 60 / 60 / 24,2)}天",
                            'time': key_data['time']})
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
    请求参数:
        rj_id: 软件id
        y: 验证器
        key: 卡类型[zk,tk,yk,nk]
        head: 谁的卡
        jie: 是否完全绑定机器码 1,0   
        num: 卡数量
    """
    y = request.args.get('y')
    rj_id = request.args.get('rj_id') or request.form.get('rj_id') or '' # 软件id
    jie = request.args.get('jie') or request.form.get('jie') or '' # 是否可以被解绑
    if not y:
        return jsonify({'msg': '错误, 此页面暂时不允许访问, 服务器内部错误'})
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
    if not k_num:
        k_num = '5'
    if k_num.isdigit() and int(k_num) > 0:
        key_num = int(k_num)
    key_list = [{'key': f'{key}{core.get_ran_str(24)}',
                 'time': 0,
                 'create_time': time.strftime("%Y-%m-%d %H:%M:%S"),
                 'rj_id': rj_id,
                 'jiqima_nojie': jie,
                 'user': head}
                for i in range(key_num)]
    key_list1 = [i['key'] for i in key_list]
    mo = MyMongo1('key')
    mo.save(key_list)
    return jsonify({'msg': 'ok', 'key_list': key_list1})


@bp.route('/getkey', methods=('GET', 'POST'))
def getkey():
    y = request.args.get('y') or request.form.get('y')
    rj_id = request.args.get('rj_id') or request.form.get('rj_id') or '' # 软件id
    if not y:
        return jsonify({'msg': '错误, 此页面暂时不允许访问, 服务器内部错误'})
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
        } for i in x if i['time'] == 0 and i.get('rj_id') == rj_id]
    elif gq == '2':
        x1 = [{
            '类型': '全部',
            'key': i['key'],
            'time': i['time'],
            'create_time': i['create_time'],
            'endtime': i.get('endtime'),
            '机器码s': i.get('jiqimas'),
        } for i in x if i.get('rj_id') == rj_id]
    elif gq == '3':
        x1 = [{
            '类型': '使用中的',
            'key': i['key'],
            'time': i['time'] - time.time(),
            'create_time': i['create_time'],
            'endtime': i.get('endtime'),
            '机器码s': i.get('jiqimas', []),
        } for i in x if i['time'] > time.time() and i.get('rj_id') == rj_id]
    else:
        x1 = []
    return jsonify({'msg': 'ok', 'key_list': x1})


@bp.route('/upkey', methods=('GET', 'POST'))
def upkey():
    """ 
    args:
        y: 验证器
        key: 卡
        time_a:
        add_time:
        jie: 解除机器码
    """ 
    y = request.args.get('y') or request.form.get('y')
    if not y:
        return jsonify({'msg': '错误, 此页面暂时不允许访问, 服务器内部错误'})
    if y != time.strftime("%d%H"):
        return jsonify({'msg': '错误, 此页面暂时不允许访问, 服务器内部错误'})
    key = request.args.get('key') or request.form.get('key')
    time_a = request.args.get('time_a') or request.form.get('time_a')
    addtime = request.args.get('addtime') or request.form.get('addtime')
    jie = request.args.get('jie') or request.form.get('jie')
    if jie:
        # TODO 解除机器码
        pass
    if time_a:
        if not (addtime and time_a and key):
            return jsonify({'msg': '参数错误'})
        mo = MyMongo1('key')
        mo_key = mo.find({'key': key})
        if not mo_key:
            return jsonify({'msg': '错误, key不存在'})
        if time_a.isdigit() and int(time_a) > 0:
            if time_a == '1':
                # 加时间
                if not (addtime.isdigit() and int(addtime) > 0):
                    return jsonify({'msg': 'addtime 错误'})
                ka_time = time.time() if mo_key['time'] < time.time(
                ) else mo_key['time']
                time_a = ka_time + 60 * 60 * 24 * int(addtime)
                mo.update({'key': key}, {'time': time_a})
                return jsonify({'msg': f'已经将他的时间增加了 {addtime} 天', 'key': key, 'time': time_a})
            if time_a == '2':
                # 将时间设置为 1
                mo.update({'key': key}, {'time': 1})
                return jsonify({'msg': '已经将他的时间清空', 'key': key})
        return jsonify({'msg': '好像什么都没发生'})


@bp.route('/getaut', methods=('GET', 'POST'))
def getaut():
    """
    获取账号 
    """
    x = get_mo_aut()
    r_data = {
        'aut': x['aut'],
        'jishu': x['jishu'],
        'create_time': x['create_time'],
        'ban': x['ban'],
    }
    return jsonify({'msg': 'ok', 'aut_list': r_data})


@bp.route('/getauts', methods=('GET', 'POST'))
def getauts():
    """
    获取账号列表
    """
    r_data = []
    mo = MyMongo1('aut')
    aut_list = mo.find_many({})
    for aut in aut_list:
        r_data.append({
            'aut': aut['aut'],
            'jishu': aut['jishu'],
            'create_time': aut['create_time'],
            'ban': aut['ban'],
        })
    return jsonify({'msg': 'ok', 'aut_list': r_data})


@bp.route('/addaut', methods=('GET', 'POST'))
def addaut():
    y = request.args.get('y') or request.form.get('y')
    if y != time.strftime("%d%H"):
        return jsonify({'msg': '错误, 此页面暂时不允许访问, 服务器内部错误'})
    aut = request.args.get('aut') or request.form.get('aut')
    jishu = request.args.get('jishu') or request.form.get('jishu') or 0
    if aut:
        mo = MyMongo1('aut')
        if mo.find({'aut': aut}):
            return jsonify({'msg': '错误, 账号已经存在'})
        mo.save({'aut': aut, 'jishu': jishu,
                'create_time': time.time(), 'ban': 0})
    return jsonify({'msg': 'ok', 'aut': aut, 'jishu': jishu})


@bp.route('/upaut', methods=('GET', 'POST'))
def upaut():
    y = request.args.get('y') or request.form.get('y')
    if y != time.strftime("%d%H"):
        return jsonify({'msg': '错误, 此页面暂时不允许访问, 服务器内部错误'})
    aut = request.args.get('aut') or request.form.get('aut')
    ban = request.args.get('ban') or request.form.get('ban') or 0
    if not ban.isdigit():
        return jsonify({'msg': 'ban 错误'})

    if aut:
        mo = MyMongo1('aut')
        mo.update({'aut': aut}, {'ban': int(ban)})
    return jsonify({'msg': 'ok', 'aut': aut, 'ban': ban})
