"""
此为ts1

ts1 用于给手机发消息的

打算链接一个 html，考虑是否搞个登录的东西
"""

from flask import Blueprint, request, jsonify, current_app, g
from app01 import myfuncs
from addict import Dict
from utils import send_email
from datetime import datetime
import time
import requests
from entities import data_saves

service_name = 'ts1'

bp = Blueprint(service_name, __name__, url_prefix='/ts1')

def send1(urls=[], data="", level=3):
    """
    args:
        urls: 要发的地址(列表)
        data: 要发的东西()
        level: 等级， 越高越重要 (1-5)
    """
    # requests.post(
    #     "https://ntfy.sh/pcn10p",
    #     data=f"{time.strftime('%X')}wx拉黑结束了 y0001 over".encode(encoding="utf-8"),
    #     headers={"Priority": "4"},
    # )
    for to_url in urls:
        requests.post(
            "https://ntfy.sh/pcn10p",
            data = data,
            headers={"Priority": "4"},
        )


@bp.route('/', methods=('GET', 'POST'))
def index():
    datas = myfuncs.get_datas(request)
    data_saves.save_data(datas, 2, 'email')
    return datas
