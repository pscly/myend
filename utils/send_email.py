import yagmail
import os
# import requests
from flask import g
from app01 import myfuncs

def send_email(body, email_data:dict={}):
    if not email_data:
        email_data = os.y.email_data
    print(email_data)
    yag = yagmail.SMTP(email_data.E_USER, email_data.E_PWD, host=email_data.E_HOST)
    ip = ''
    send_data = ['pscly@qq.com', '来自my_end,', body]
    myfuncs.write_data({'send_data': send_data, 'who': 'email'})
    
    try:
        yag.send(*send_data)
        return True
    except Exception as e:
        print(e)
        return False


def get_ip():
    res1 = requests.get("pscly.cn:31001/md")



    

