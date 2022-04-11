import yagmail
import os
# import requests
from flask import g

def send_email(body, email_data:dict={}):
    # key = UXQSTCRIEKULJEDL

    yag = yagmail.SMTP('pscly1@163.com', 'UXQSTCRIEKULJEDL', host='smtp.163.com')
    # yag = yagmail.SMTP(email_data['addr'], email_data['key'], host='smtp.163.com')
    ip = ''
    try:
        yag.send('pscly@qq.com', '来自my_end,', body)
        return True
    except Exception as e:
        print(e)
        return False


def get_ip():
    res1 = requests.get("pscly.cn:31001/md")



    

