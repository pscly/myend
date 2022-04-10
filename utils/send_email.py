import yagmail
import os
import requests
from flask import g

def send_email(email_address, subject, body, email_data:dict):
    yag = yagmail.SMTP(email_data['addr'], email_data['key'], host='smtp.163.com')
    text = ['python测试1 ', '01点45分', '333333']
    ip = ''
    try:
        yag.send('pscly@qq.com', '来自my_end,', text)
        return True
    except Exception as e:
        print(e)
        return False

# def get_ip():
    
    

print(x,'a')
print('adsf')

