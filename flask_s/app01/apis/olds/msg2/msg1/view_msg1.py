"""
此为msg1

msg1 用于给手机发消息的

打算链接一个 html，考虑是否搞个登录的东西


通过用户查询有哪些设备，可以添加设备
可以定时发送
可以写记录

"""
import os
import random
import time
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
from utils.up_dns import up_dns1

service_name = "msg1"

bp = Blueprint(service_name, __name__, url_prefix="/msg1")


def get_user_devices(user, format1=True):
    """
    通过链接数据库，获取用户的设备
    """
    mo = MyMongo1("msg1_user_devices")
    devices = [x for x in mo.find_many({"user": user})]
    if format1:
        user_devices = {}
        for device in devices:
            if device.get("device_name"):
                user_devices[device.get("device_name")] = Dict(device)
        return user_devices
    return devices


def add_user_device(user, device_name, device_url):
    """
    传入设备, 然后保存到数据库
    """
    mo = MyMongo1("msg1_user_devices")
    save_data = {
        "user": user,
        "device_name": device_name,
        "device_url": device_url,
        "add_time": datetime.now(),
        "time2": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    }
    mo.save(save_data)


def remove_user_device(user, device_name):
    mo = MyMongo1("msg1_user_devices")
    mo.delete({"user": user, "device_name": device_name})


def send_data(urls=[], data="", level=3):
    """
    args:
        urls: 要发的地址(列表)
        data: 要发的东西()
        level: 等级， 越高越重要 (1-5)
    """
    for to_url in urls:
        requests.post(
            to_url,
            data=data,
            headers={"Priority": str(level)},
        )


@bp.route("/", methods=("GET", "POST"))
def index():
    datas = myfuncs.get_datas(request)
    if not current_user.is_authenticated:
        return redirect(url_for("/.index"))

    user = current_user.id
    # send_data(["https://ntfy.sh/pcmym13u", "https://ntfy.sh/pchy"], "nihao", 4)
    return render_template(
        "msg1_1.html",
        all_data={
            "page_": "消息推送中心",
            "user_devices": get_user_devices(user, 0),
        },
    )


@bp.route("/add/", methods=("GET", "POST"))
def add():
    datas = myfuncs.get_datas(request)
    if not current_user.is_authenticated:
        return redirect(url_for("/.index"))

    user = current_user.id
    user_devices = get_user_devices(user)

    if request.method == "POST":
        device_name = request.form.get("name")
        device_url = request.form.get("url")
        if device_name in user_devices:
            return render_template(
                "msg1_add.html",
                all_data={
                    # "page_": "消息推送中心_添加设备",
                    "err1": f"{device_name} 设备已存在",
                },
            )
        add_user_device(user, device_name, device_url)
        return render_template(
            "msg1_add.html",
            all_data={
                "page_": f"{device_name} 设备添加成功",
            },
        )

    return render_template(
        "msg1_add.html",
        all_data={
            "page_": "消息推送中心_添加设备",
        },
    )


@bp.route("/del/", methods=("GET", "POST"))
def del_devices():
    """
    todo 2023-07-17 16:36:05
    还没做完逻辑
    """
    datas = myfuncs.get_datas(request)
    if not current_user.is_authenticated:
        return redirect(url_for("/.index"))

    user = current_user.id
    user_devices = get_user_devices(user)

    if request.method == "POST":
        device_name = request.form.get("name")
        if not device_name:
            return render_template(
                "msg1_del.html",
                all_data={
                    "err1": "设备名不能为空",
                    "user_devices": get_user_devices(user, 0),
                },
            )
        if device_name not in user_devices:
            return render_template(
                "msg1_del.html",
                all_data={
                    "err1": f"{device_name} 设备不存在",
                    "user_devices": get_user_devices(user, 0),
                },
            )
        remove_user_device(user, device_name)
        return render_template(
            "msg1_del.html",
            all_data={
                "err1": f"{device_name} 删除成功",
                "user_devices": get_user_devices(user, 0),
            },
        )
    return render_template(
        "msg1_del.html",
        all_data={
            "user_devices": get_user_devices(user, 0),
        },
    )
