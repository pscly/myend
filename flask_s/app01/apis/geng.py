
from flask import Blueprint, redirect, request, g, render_template, render_template, jsonify
from entities import data_saves
from .. import myfuncs
import time
import random
from entities.mymongo import MyMongo1
from addict import Dict
from entities import data_saves
from utils.up_dns import up_dns1
import os

service_name = '/'
bp = Blueprint(service_name, __name__)


@bp.route('/', methods=['GET'])
def index():
    data = myfuncs.get_datas(request)
    data_saves.save_data(data, 1, 'gen')
    yyids = [
        28188427,
        1407112865,
        1919147134,
        1453957944,
        1886371886,
        450853439
    ]
    return render_template('geng.html', yyid=random.choice(yyids), imgid=str(random.randint(1, 18)), beian=os.y.data2.BEIAN)
    # return render_template('down.html', files=files, imgid=str(random.randint(1, 18)))
    # return render_template('down.html', datas={"files": files, "imgid": random.randint(1, 18)})


@bp.route('/robot.txt', methods=['GET'])
def robot():
    data = myfuncs.get_datas(request)
    data_saves.save_data(data, 1, 'robot')
    return 'User-agent: *\nDisallow: /'


@bp.route('/md', methods=['GET'])
def md():
    data = myfuncs.get_datas(request)
    data_saves.save_data(data, 1, 'gen')
    return data

@bp.route('/ddns', methods=['GET', 'POST'])
def ddns():
    # ip = request.remote_add
    ip = request.args.get('ip') or request.form.get('ip') or request.headers.get('X-Forwarded-For', request.remote_addr)
    name = request.args.get('name') or request.form.get('name')
    y = request.args.get('y') or request.form.get('y') or ''
    v = request.args.get('v') or request.form.get('v') or ''
    if not (name and ip):
        return jsonify({'code': 1, 'msg': '参数错误'})
    dns_type = 'A'
    if v == '6':
        dns_type = 'AAAA'
            
    # 连接 mongo 数据库
    mo = MyMongo1('ddns')
    # d1 = {'time': time.time()}
    # mo.save(d1)
    ip_dns = Dict(mo.find({'name': name}))
    if not ip_dns:
        d1 = Dict({'name': name, 'ip': ip, 'time': time.strftime('%Y-%m-%d %X'), 'ips': [{'time':time.time(), 'ip':ip}]})
        mo.save(d1)
        ip_dns = d1

    if ip != ip_dns.ip:
        # 发送邮件警报
        email_msg = Dict({'msg': f'-> {name} -< ip update, {ip_dns.ip} --->  {ip}'})
        ip_dns.ips.append({'time':time.strftime('%Y-%m-%d %X'), 'ip':ip})
        ip_dns.ip = ip
        # 自动更新
        if (time.strftime('%H%d%M') in y) and os.y.y != y:  # 如果 y 的时间是正确的, 并且 y 没有被用过
            os.y.y = y
            ym = request.args.get('ym') or request.form.get('ym') or 'pscly.cn'
            ym_id = request.args.get('ym_id') or request.form.get('ym_id')
            if not (ym and ym_id):
                jsonify({'code': 1, 'msg': 'ym or ym_id 参数错误'})
            up_dns1(ym, name, ym_id, ip,dns_type=dns_type)
            email_msg.updns = True
            # data_saves.save_data(email_msg, 2, 'ddns')
            mo.save(ip_dns)
            ip_dns.pop('_id')   # 这是 mongo 的 id, 不需要返回给用户
            return jsonify({'code': 1, 'msg': 'ip变化', 'ip_dns': ip_dns})
    return jsonify({'code': 0, 'msg': 'ok'})
    # if not aut_list:
        
        

@bp.route('/emi/', methods=['GET', 'POST'])
def emi():
    # 带着arg和postdata跳转到email模块
    # print(app.config)
    return redirect('/email/', request.base_url)
