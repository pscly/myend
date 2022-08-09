from app01.apis.geng import bp as geng_bp
from app01.apis.end1.view_end1 import bp as end1_bp
from app01.apis.email.view_email import bp as emi_bp
from app01.apis.files.view_files import bp as files_bp
from app01.apis.rum.view_rum import bp as rum_bp
from app01.apis.texts.view_text import bp as texts_bp
from app01.apis.to_video.view_video import bp as to_v_bp

routers = [
    geng_bp,        # 根路由
    end1_bp,        # 后端1的路由
    emi_bp,         # 邮件路由
    files_bp,       # 文件共享路由
    rum_bp,         # rum 相关
    texts_bp,         # rum 相关
    to_v_bp,         # to_v 相关
]
