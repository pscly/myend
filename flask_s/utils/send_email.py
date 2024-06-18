import yagmail
import os
import requests
from flask import g
import json
from addict import Dict


def send_email(body, email_data: dict = {}, email_addr: str = ""):
    if not isinstance(email_data, dict) or (email_data.get("E_USER", '') == ''):
        email_data = os.y.data2
        if os.y.data2.get("E_USER", '') == '':
            print("没配置EMAIL")
            return False
    yag = yagmail.SMTP(email_data.E_USER, email_data.E_PWD, host=email_data.E_HOST)
    send_data = ["pscly@qq.com", "来自my_end,", body]
    if email_addr:
        send_data[0] = email_addr
    send_data[2] = json.dumps(send_data[2], ensure_ascii=False, indent=4)
    try:
        yag.send(*send_data)
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    email_data = Dict(
        {"E_USER": "pscly1@163.com", "E_PWD": "x", "E_HOST": "smtp.163.com"}
    )  # {'E_USER':'','E_PWD':'','E_HOST':''}
    send_email("abc", email_data)
