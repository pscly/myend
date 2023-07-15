from datetime import datetime

# from funcs1 import ProxyServer,t
# from bl import a1
from addict import Dict
import os
import time
import re
import json
import requests


def deadlines(year=2022, mouth=6, day=30):
    now = datetime.now().timestamp()
    now2 = requests.get("http://pscly.cn:31002/md").json()["time2"]
    expire = datetime(year, mouth, day, 0, 0).timestamp()
    res = expire - now2
    if res < 0:
        print("软件版本过低，请更新")
        raise Exception("error")


def close_proxy():
    os.system(
        'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f '
    )
    os.system(
        'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /d "" /f'
    )
    os.system(
        'reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /f'
    )
    print("ok2")


def yz():
    if os.environ.get("osy") != "y":
        close_proxy()
        return True
    deadlines(mouth=9, day=10)


if __name__ == "__main__":
    # yz()
    net_yz(Dict({"激活码": "yk1ek5smcfig8y0xwpa6r7qlhj"}))
