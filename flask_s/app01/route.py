from app01.apis.geng import bp as geng_bp
from app01.apis.end1.view_end1 import bp as end1_bp
from app01.apis.email.view_email import bp as emi_bp
from app01.apis.files.view_files import bp as files_bp

routers = [
    geng_bp,        # 根路由
    end1_bp,        # 后端1的路由
    emi_bp,         # 邮件路由
    files_bp,       # 文件共享路由
]
