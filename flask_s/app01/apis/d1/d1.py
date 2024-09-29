"""
此为msg2

用于用钉钉发消息

"""

import os
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
def send_message():
    datas = myfuncs.get_datas(request)
    message_type = datas.get('data', {}).get('type')
    bt = datas.get('data', {}).get('bt')
    content = datas.get('data', {}).get('content')
    
    if bt:
        xiaoding.send_markdown(title=bt, text=content)
    else:
        send_data = f"""
# 消息(no 标题)
```json
{json.dumps(datas, ensure_ascii=False, indent=4)}
```
"""
        xiaoding.send_markdown(title="无标题的消息", text=send_data)
    
    return jsonify({"message": "已经尝试发送消息了"}), 200


