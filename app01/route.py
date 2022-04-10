from app01.apis.geng import bp as geng_bp
from app01.apis.end1.view_end1 import bp as end1_bp
from app01.apis.email.view_email import bp as emi_bp

routers = [
    geng_bp,
    end1_bp,
    emi_bp,
]
