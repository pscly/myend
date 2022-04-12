import yagmail
import os
import requests
from flask import g
import json

def send_email(body, email_data:dict={}):
    if not email_data:
        email_data = os.y.email_data
    yag = yagmail.SMTP(email_data.E_USER, email_data.E_PWD, host=email_data.E_HOST)
    ip = get_ip()
    send_data = ['pscly@qq.com', '来自my_end,', body]
    
    try:
        yag.send(*send_data)
        return True
    except Exception as e:
        print(e)
        return False
