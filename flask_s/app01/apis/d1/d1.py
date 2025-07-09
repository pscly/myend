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
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=这里填写自己钉钉群自定义机器人的token'
secret = 'SEC11b9...这里填写自己的加密设置密钥'  # 可选：创建机器人勾选“加签”选项时使用
# 初始化机器人小丁
xiaoding = DingtalkChatbot(webhook)  # 方式一：通常初始化方式
xiaoding = DingtalkChatbot(webhook, secret=secret)  # 方式二：勾选“加签”选项时使用（v1.5以上新功能）
xiaoding = DingtalkChatbot(webhook, pc_slide=True)  # 方式三：设置消息链接在PC端侧边栏打开（v1.5以上新功能）

## markdown 消息举例

xiaoding.send_markdown(title='氧气文字', text='#### 广州天气 @1882516xxxx\n'
                       '> 9度，西北风1级，空气良89，相对温度73%\n\n'
                       '> ![美景](http://www.sinaimg.cn/dy/slidenews/5_img/2013_28/453_28488_469248.jpg)\n'
                       '> ###### 10点20分发布 [天气](http://www.thinkpage.cn/) \n',
                       at_mobiles=at_mobiles)

我的
webhook = "https://oapi.dingtalk.com/robot/send?access_token=62bd90531b3260a49f6f9f33b645ae0fdbc6a40094ec7f668254326f5a422590"
secret = "SEC03d2b63a1495d35b199980c73a6b46a0ed0eb8f2c879df0dd4e0a400a6c5bc17"

"""

service_name = "d1"

bp = Blueprint(service_name, __name__, url_prefix=f"/{service_name}")

webhook = "https://oapi.dingtalk.com/robot/send?access_token=62bd90531b3260a49f6f9f33b645ae0fdbc6a40094ec7f668254326f5a422590"
secret = "SEC03d2b63a1495d35b199980c73a6b46a0ed0eb8f2c879df0dd4e0a400a6c5bc17"
xiaoding = DingtalkChatbot(webhook, secret=secret)

@bp.route("/", methods=["POST", "GET"])
@bp.route("", methods=["POST", "GET"])
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
    
    # if data is None:
        # 如果不是JSON，就从 values (form 或 args) 中获取
        # data = request.values.to_dict()

    content = f"# {bt}\n\n{content}\n\n---\n\n> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
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


