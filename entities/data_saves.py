"""此文件是为了将数据持久化存储或将数据发送到特定目标
"""

from app01 import myfuncs
from utils import send_email
from utils import core
from addict import Dict
import time
import threading

def save_data(data:dict, level:int, who:str):
    """
    保存数据
    :param data: dict
    :param int: 1 是只保存数据，2是保存数据并发送邮件
    :return:
    """
    data = Dict(data)
    if level >= 2:
        threading.Thread(target=send_email.send_email, args=(data,)).start()
    myfuncs.write_data(data)
