# coding: utf-8
# START-DATE: 2021-08-07 23:58
# END-DATE: 
# 
import os
from flask import *
from utils import factory


app = factory.create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 31001))    # 这个port应该是从配置里面拿的

    app.run(host='0.0.0.0', port=port, threaded=True)

