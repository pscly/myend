"""
此为msg2

用于支付，

"""

import os
import random
import time
import hashlib
import urllib.parse
from datetime import datetime


import requests
from addict import Dict
from flask import (
    Blueprint,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from app01 import myfuncs
from entities import data_saves
from entities.mymongo import MyMongo1
from utils import send_email
from utils.core import hash_password, verify_password
from utils.login1 import User, get_one_user, save_one_user
from utils.up_dns import up_dns1
from utils.db import get_db
from utils.database import db_session
from entities.pgmodels import AppConfig

service_name = "pays"

bp = Blueprint(service_name, __name__, url_prefix="/pays")


# def get_user_devices(user, format1=True):
#     """
#     通过链接数据库，获取用户的设备
#     """
#     mo = MyMongo1("msg1_user_devices")
#     devices = [x for x in mo.find_many({"user": user})]
#     if format1:
#         user_devices = {}
#         for device in devices:
#             if device.get("device_name"):
#                 user_devices[device.get("device_name")] = Dict(device)
#         return user_devices
#     return devices


# def add_user_device(user, device_name, device_url):
#     """
#     传入设备, 然后保存到数据库
#     """
#     mo = MyMongo1("msg1_user_devices")
#     save_data = {

#         "user": user,
#         "device_name": device_name,
#         "device_url": device_url,
#         "add_time": datetime.now(),
#         "time2": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
#     }
#     mo.save(save_data)


# 生成订单号
def get_order_id(add_txt):
    date1 = (
        time.strftime("%Y%m%d%H%M%S", time.localtime())
        + "0"
        + str(add_txt)
        + str(random.randint(100, 999))
    )
    return date1


def remove_user_device(user, device_name):
    mo = MyMongo1("msg1_user_devices")
    mo.delete({"user": user, "device_name": device_name})


def format_money(pay_money):
    try:
        # 尝试将 pay_money 转换为浮点数
        float_money = float(pay_money)
        # 格式化为两位小数的字符串
        formatted_money = f"{float_money:.2f}"
        return formatted_money
    except ValueError:
        # 如果转换失败，返回原始字符串的前部分
        return pay_money.split(".")[0] + ".00"


def get_sign_from_query_string(query_string, key):
    # 解析查询字符串
    param = dict(urllib.parse.parse_qsl(query_string))
    # 排序参数
    sorted_param = dict(sorted(param.items()))
    # 构造签名字符串
    signstr = ""
    for k, v in sorted_param.items():
        if k != "sign" and k != "sign_type" and v != "":
            signstr += f"{k}={v}&"
    # 去掉最后一个 '&'
    if signstr:
        signstr = signstr[:-1]
    # 添加密钥
    signstr += key
    # 计算MD5哈希值
    sign = hashlib.md5(signstr.encode("utf-8")).hexdigest()
    return sign


@bp.route("/", methods=("GET", "POST"))
def index():
    # 这里只是一个对应表，方便后面直接拿去，前端请求就只需要带个编号过来就行
    pay_dic = {
        "1": ["alipay", "支付宝"],
        "2": ["wxpay", "微信支付"],
        "3": ["qqpay", "QQ钱包"],
        "4": ["tenpay", "财付通"],
    }

    datas = myfuncs.get_datas(request)
    data1 = datas.get("data")
    pay_money = data1.get("money")
    p_type = data1.get(
        "p_type"
    )  # 支付类型 alipay:支付宝,tenpay:财付通, qqpay:QQ钱包,wxpay:微信支付
    if (not pay_money) or (not p_type or not p_type in pay_dic):
        return render_template(
            "404.html",
            msg="支付失败，参数错误 p_type  money",
        )

    pay_type = pay_dic.get(p_type)[0]

    pay_size_url = str(os.y.data2.get("PAY_URL"))
    pay_pid = str(os.y.data2.get("PAY_PID"))
    pay_key = str(os.y.data2.get("PAY_KEY"))
    pay_pid = "153457828"
    pay_key = "a2kK3DZ7jHHg7e3EGe6dE1dkGg2A2B87"
    server_url = str(os.y.data2.get("SERVER_URL"))
    notify_url = server_url + "/pays/notify"
    # 商品名称 = '激活卡'
    name_1 = "vip会员"
    web_name = "yend"
    order_id = get_order_id(str(pay_money))

    # # 更新一下这里，如果 pay_money 已经有小数点并且是金钱的那种两位小数的话，就不再加了, 如果不是，例如10.1 那么就加个 .0 变成 10.10，反正补充为货币那种保留两位小数点，如果是11.12.13 那么就只要前面的 11.12 这种
    pay_money = format_money(pay_money)

    url_1 = f"money={pay_money}&name={name_1}&notify_url={notify_url}&out_trade_no={order_id}&pid={pay_pid}&return_url={server_url}&type={pay_type}&key={pay_key}"
    sign = get_sign_from_query_string(url_1, pay_key)
    pay_url = pay_size_url + "/api.php?" + url_1 + "&sign=" + sign + "&sign_type=MD5"
    for _ in range(10):
        pay_res = requests.get(pay_url, proxies={}, verify=False)
        if pay_res and pay_res.status_code == 200:
            pay_res_json = Dict(pay_res.json())
            if pay_res_json.orderid:
                return redirect(
                    f"https://xy.znxo.cn/Submit/Mcode_Pay.php?trade_no={pay_res_json.orderid}"
                )
        time.sleep(0.5)

    return render_template(
        "404",
        all_data={
            "msg": "支付失败，系统错误",
        },
    )


@bp.route("/any/", methods=("GET", "POST"))
def any_pay():
    """
    这个和上一个的区别是这个的参数只有通道，具体金额的话是让客户自己在网页里面填
    """
    pay_dic = {
        "1": ["alipay", "支付宝"],
        "2": ["wxpay", "微信支付"],
        "3": ["qqpay", "QQ钱包"],
        "4": ["tenpay", "财付通"],
    }

    datas = myfuncs.get_datas(request)
    data1 = datas.get("data")
    p_type = data1.get("p_type")
    if (not p_type) or (not p_type in pay_dic):
        return render_template(
            "404.html",
            msg="支付失败，参数错误_ p_type  money",
        )
    return render_template("anypay.html")


@bp.route('/config', methods=['GET', 'POST'])
def config():
    with db_session() as session:
        if request.method == 'POST':
            data = request.json
            config = AppConfig(**data)
            session.add(config)
            return jsonify({"message": "Config saved successfully"}), 200
        else:
            configs = session.query(AppConfig).all()
            return jsonify([config.to_dict() for config in configs]), 200
