from app01.apis.geng import bp as geng_bp
from app01.apis.end1.view_end1 import bp as end1_bp
from app01.apis.email.view_email import bp as emi_bp
from app01.apis.files.view_files import bp as files_bp
from app01.apis.files.view_files2 import bp as files2_bp
# from app01.apis.rum.view_rum import bp as rum_bp
# from app01.apis.texts.view_text import bp as texts_bp
# from app01.apis.datas.view_data import bp as datas_bp
# from app01.apis.to_video.view_video import bp as to_v_bp    # 一次性播放视频的
from app01.apis.to_url.view_url import bp as to_url_bp      # xl 一次性网页
# from app01.apis.msg1.view_msg1 import bp as msg1_bp       # 手机消息
# from app01.apis.msg2.view_msg2 import bp as msg2_bp         # 钉钉消息
# from app01.apis.qita.ddns import bp as ddns_bp              # ddns
from app01.apis.pays.payindex import bp as paypb              # ddns
from app01.apis.d1.d1 import bp as d1_bp              # 用钉钉发消息
from app01.apis.w1.w1 import bp as w1_bp              # 用钉钉发消息


routers = [
    geng_bp,  # 根路由
    end1_bp,  # 后端1的路由
    emi_bp,  # 邮件路由
    files_bp,  # 文件共享路由
    # files2_bp,  # 文件共享路由
    # rum_bp,  # rum 相关
    # texts_bp,  # rum 相关
    # datas_bp,  # rum 相关
    # to_v_bp,  # to_v 相关
    # to_url_bp,  # to_v 相关
    # msg1_bp,  # 手机消息 相关
    # msg2_bp,  # 钉钉消息 相关
    paypb,  # 支付 相关
    d1_bp,  # 用钉钉发消息
    w1_bp,  # 用企业微信发消息
]
