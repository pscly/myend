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
    date1 = time.strftime("%Y%m%d%H%M%S", time.localtime()) + "0" + str(add_txt) +str(random.randint(100, 999))
    return date1

def remove_user_device(user, device_name):

    mo = MyMongo1("msg1_user_devices")
    mo.delete({"user": user, "device_name": device_name})

def get_msg_md5(text):
    """
    签名 

    使用的是支付宝的
    
    筛选 获取所有请求参数，不包括字节类型参数，如文件、字节流，剔除sign与sign_type参数。

    排序 将筛选的参数按照第一个字符的键值ASCII码递增排序（字母升序排序），如果遇到相同字符则按照第二个字符的键值ASCII码递增排序，以此类推。

    拼接 将排序后的参数与其对应值，组合成“参数=参数值”的格式，并且把这些参数用&字符连接起来，此时生成的字符串为待签名字符串。MD5签名的商户需要将key的值拼接在字符串后面，调用MD5算法生成sign；RSA签名的商户将待签名字符串和商户私钥带入SHA1算法中得出sign。 商户如用支付宝提供的demo集成，demo已写好签名验签的方法，商户可直接调用，如自己开发不用demo，则按以上方法拼接待签名字符串。 以下是待签名字符串的示例，key值已被隐藏，参数值都是示例不是真实的，商户参考格式即可：

    money: 35
    name: 天卡：5E项目IG
    notify_url: https://ergouzi.50oo.cn/s/other/epay_notify.php
    out_trade_no: 20240921145719211
    pid: 1000
    return_url: https://ergouzi.50oo.cn/s/other/epay_return.php
    sitename: 1
    type: alipay
    
    money=35&name=%E5%A4%A9%E5%8D%A1%EF%BC%9A5E%E9%A1%B9%E7%9B%AEIG&notify_url=https%3A%2F%2Fergouzi.50oo.cn%2Fs%2Fother%2Fepay_notify.php&out_trade_no=20240921145719211&pid=1000&return_url=https%3A%2F%2Fergouzi.50oo.cn%2Fs%2Fother%2Fepay_return.php&sitename=1&type=alipay&sign=0fcbb2d949c888790e7500d461ba0eac&sign_type=MD5

    > 0fcbb2d949c888790e7500d461ba0eac
    
    """"""
    """
    args = text.split("&")
    args.sort()
    args_str = "&".join(args)
    args_str = args_str

    return hashlib.md5(args_str.encode()).hexdigest()

def get_sign_from_query_string(query_string, key):
    # 解析查询字符串
    param = dict(urllib.parse.parse_qsl(query_string))
    
    # 排序参数
    sorted_param = dict(sorted(param.items()))
    
    # 构造签名字符串
    signstr = ''
    for k, v in sorted_param.items():
        if k != "sign" and k != "sign_type" and v != '':
            signstr += f'{k}={v}&'
    
    # 去掉最后一个 '&'
    if signstr:
        signstr = signstr[:-1]
    
    # 添加密钥
    signstr += key
    
    # 计算MD5哈希值
    sign = hashlib.md5(signstr.encode('utf-8')).hexdigest()
    
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
    data1 = datas.get('data')
    pay_money = data1.get('money')
    p_type = data1.get('p_type')     # 支付类型 alipay:支付宝,tenpay:财付通, qqpay:QQ钱包,wxpay:微信支付
    if (not pay_money) or (not p_type or not p_type in pay_dic):
        return render_template(
            "404.html",
            msg="支付失败，参数错误",
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
    name_1 = 'vip会员'
    web_name = 'yend'
    
    order_id = get_order_id(str(pay_money))

    pay_money = str(pay_money) + ".00"
    

    # md5 data
    # (money={商品金额}&name={商品名称}& notify_url={异步通知地址}&out_trade_no={商户订单号}&pid={商户ID}&return_url={同步通知地址}&sitename={站点名称}&type={支付方式}{商户密匙})
    url_1 = f"money={pay_money}&name={name_1}&notify_url={notify_url}&out_trade_no={order_id}&pid={pay_pid}&return_url={server_url}&type={pay_type}&key={pay_key}"
    # sign = get_msg_md5(url_1)
    sign = get_sign_from_query_string(url_1, pay_key)
    
    # 发起支付请求

    # url_pay/submit.php?pid={商户ID}&type={支付方式}&out_trade_no={商户订单号}&notify_url={服务器异步通知地址}&return_url={页面跳转通知地址}&name={商品名称}&money={金额}&sitename={网站名称}&sign={签名字符串}&sign_type=MD5

    pay_url = pay_size_url + '/api.php?' + url_1 + '&sign=' + sign + '&sign_type=MD5'
    print(pay_url)
    # https://xy.znxo.cn/api.php?money=100.00&name=vip%E4%BC%9A%E5%91%98&notify_url=https://pscly.cc/pays/notify&out_trade_no=202409211450450100666&pid=153457828&return_url=https://pscly.cc&sitename=yend&type=alipay&key=a2kK3DZ7jHHg7e3EGe6dE1dkGg2A2B87&sign=ff2d5641345928c0f55b8dc9cdcc0aea&sign_type=MD5
    # https://xy.znxo.cn/submit.php?money=100.00&name=vip会员&notify_url=https://pscly.cc/pays/notify&out_trade_no=202409211506090100585&pid=153457828&return_url=https://pscly.cc&type=alipay&key=a2kK3DZ7jHHg7e3EGe6dE1dkGg2A2B87&sign=0d527e2e20b7037640fb476213b93c23&sign_type=MD5

    for _ in range(10):    
        pay_res = requests.get(pay_url, proxies={}, verify=False)
        if pay_res and pay_res.status_code == 200:
            pay_res_json = Dict(pay_res.json())
            if pay_res_json.orderid:
                return redirect(f'https://xy.znxo.cn/Submit/Mcode_Pay.php?trade_no={pay_res_json.orderid}')
        time.sleep(1)

    return render_template(
        "404",
        all_data={
            "msg": "支付失败，系统错误",
        },
    )


