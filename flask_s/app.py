# coding: utf-8
# START-DATE: 2021-08-07 23:58
# END-DATE:
#
import os
from flask import current_app
from utils import factory
from utils import core
from addict import Dict
from utils import send_email
import time
import threading

# 读取配置
os.y = Dict()
os.y.email_data = Dict(core.load_config_yaml('y_data.yaml', mode='COMMON') or
                       {'E_USER': '', 'E_PWD': '', 'E_HOST': ''})  # {'E_USER':'','E_PWD':'','E_HOST':''}
app = factory.create_app()

if __name__ == '__main__':
    # port = int(current_app.config.get('PORT', 31001))    # 这个port应该是从配置里面拿的
    port = app.config.get('PORT', 31001)
    threading.Thread(target=send_email.send_email, args=({"time": time.strftime("%Y-%m-%d %X"),
                                                          'data': 'server_myend_runing',
                                                          'server': os.environ.get('NODETYPE')},)).start()
    app.run(host='0.0.0.0', port=port, threaded=True)
