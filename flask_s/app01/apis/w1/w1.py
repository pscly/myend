"""
此为msg2

用于用钉钉发消息

"""

import os
import re
import random
import time
import json
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
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, CardItem

"""
这东西只可以可信ip发送

企业微信发消息， 只能txt， markdown 的话微信不显示

curl -X POST 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=kMr6Ud1bxegttQnyoMALOCa62ad-osnPWfreikrTTNwFxdo_uScbhy6LWofl8MNZRy9z7-gl7qgHoimF6f2QUhY2X6lFtfYEJyop7ep5N6YPdGir1k0Vb6IpKPD0DozHEoSi1WDJrOrGUUibGHffZ6Y1UhcXk5WmmVl0eX-2NUS3vjIiTKl-tyHj9AiEgAMDAXk4n26fa9hHc_4uHRASCQ' -H 'Content-Type: application/json' -d '{
   "touser" : "ChenLiYuan",
   "msgtype": "text",
   "agentid" : 1000004,
   "text": {
        "content": "# 消息测试test \n\n > test1"
   },
   "enable_duplicate_check": 0,
   "duplicate_check_interval": 1800
}'

"""

service_name = "w1"

bp = Blueprint(service_name, __name__, url_prefix=f"/{service_name}")

webhook = "https://oapi.dingtalk.com/robot/send?access_token=62bd90531b3260a49f6f9f33b645ae0fdbc6a40094ec7f668254326f5a422590"
secret = "SEC03d2b63a1495d35b199980c73a6b46a0ed0eb8f2c879df0dd4e0a400a6c5bc17"
xiaoding = DingtalkChatbot(webhook, secret=secret)

@bp.route("/", methods=["POST", "GET"])
def send_message():
    """
    发送消息到钉钉群的接口

    此接口接收POST或GET请求，用于发送消息到指定的钉钉群。

    请求参数:
    - bt (str, 可选): 消息标题
    - content (str 或 dict): 消息内容

    返回:
    - JSON对象:
        - message (str): 操作结果描述
        - 消息内容是 (str): 发送的消息内容
        - 标题是 (str): 发送的消息标题

    使用方法:
    1. 如果提供了 'bt' (标题)，将使用markdown格式发送消息，标题为 'bt'，内容为 'content'
    2. 如果没有提供 'bt'，将把整个请求数据作为JSON发送，标题默认为 "无标题的消息(json)"

    注意:
    - 本接口使用了钉钉机器人API，确保 webhook 和 secret 已正确配置
    - 消息发送是同步的，可能会影响接口响应时间
    """

    
    datas = request.get_json(silent=True)    
    if not datas:
        datas = myfuncs.get_datas(request)

    bt = datas.get('data', {}).get('bt')
    content = datas.get('data', {}).get('content') or datas.get('data', {})
    
    content = f"# {bt}\n\n{content}\n\n---\n\n> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=kMr6Ud1bxegttQnyoMALOCa62ad-osnPWfreikrTTNwFxdo_uScbhy6LWofl8MNZRy9z7-gl7qgHoimF6f2QUhY2X6lFtfYEJyop7ep5N6YPdGir1k0Vb6IpKPD0DozHEoSi1WDJrOrGUUibGHffZ6Y1UhcXk5WmmVl0eX-2NUS3vjIiTKl-tyHj9AiEgAMDAXk4n26fa9hHc_4uHRASCQ"

    jqrid = datas.get('jqrid') or 1000004
    try:
        jqrid = int(jqrid)
    except:
        jqrid = 1000004
        content += '\n\n 你提供了一个错误的jqrid，现在用的是默认jqrid'
        pass

    payload = {
    "touser": "ChenLiYuan",
    "msgtype": "text",            # 
    "agentid": datas.get('jqrid'),           # 机器人id
    "text": {
        "content": content,
    },
    "enable_duplicate_check": 0,
    "duplicate_check_interval": 1800
    }

    headers = {
    'Content-Type': "application/json"
    }
    requests.post(url, data=json.dumps(payload), headers=headers)

    return jsonify({
        "message": "已经尝试发送消息了", 
        "消息内容是": content,
            }), 200




@bp.route("/wifi", methods=["POST", "GET"])
def send_message_wifi():
    """
        
        这个专门用于wifi推送的
        发送消息到钉钉群的接口

        此接口接收POST或GET请求，用于发送消息到指定的钉钉群。

        请求参数:
        - bt (str, 可选): 消息标题
        - content (str 或 dict): 消息内容

        返回:
        - JSON对象:
            - message (str): 操作结果描述
            - 消息内容是 (str): 发送的消息内容
            - 标题是 (str): 发送的消息标题

        使用方法:
        1. 如果提供了 'bt' (标题)，将使用markdown格式发送消息，标题为 'bt'，内容为 'content'
        2. 如果没有提供 'bt'，将把整个请求数据作为JSON发送，标题默认为 "无标题的消息(json)"

        注意:
        - 本接口使用了钉钉机器人API，确保 webhook 和 secret 已正确配置
        - 消息发送是同步的，可能会影响接口响应时间
    """

    
    datas = myfuncs.get_datas(request)
    bt = datas.get('data', {}).get('bt')
    content = datas.get('data', {}).get('content') or datas.get('data', {})
    if request.json and request.json.get('content'):
        content = request.json.get('content')

    content = f"# {bt}\n\n{content}\n\n---\n\n> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    """
    通过正则修改
    
    <b>内容1</b>
     - 设备1
     - 设备2
    ----
    <b>内容2</b>
        - 设备3
        - 设备4
        
    改为
    
    - 内容1
        - 设备1
        - 设备2
    - 内容2
        - 设备3
        - 设备4
    """
    content = re.sub(r"<b>(.*?)</b>", r"- \1", content)
    content = re.sub(r"----", "", content)

    """
        
        - 当前有 3 台在线设备，具体如下
            IP 地址         在线时间   客户端名
            192.168.4.10   2天12小时  PCCY LAN
            192.168.4.146  2天12小时  Evan
            192.168.4.159  2天12小时  小爱音响
        
        改成
        
        - 当前有 3 台在线设备，具体如下
            - IP 地址         在线时间   客户端名
            -  192.168.4.10, 2天12小时,  PCCY LAN
            -  192.168.4.146, 2天12小时,  Evan
            -  192.168.4.159, 2天12小时,  小爱音响

    """
    content = re.sub(r"(IP 地址.*?)", r"- \1", content)
    content = re.sub(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+天\d+小时)\s+(\w+)", r"- \1, \2, \3", content)
    
    

    if bt:
        xiaoding.send_markdown(title=bt, text=content)
    else:
        send_data = f"""
# 消息(no 标题)
```json
{json.dumps(datas, ensure_ascii=False, indent=4)}
```
"""     
        bt = "无标题的消息(json)"
        xiaoding.send_markdown(title=bt, text=send_data)
        content = send_data
    
    return jsonify({
        "message": "已经尝试发送消息了", 
        "消息内容是": content,
        "标题是": bt,
            }), 200


