# extensions.py
from flask_login import LoginManager
from entities.models import Users, get_session

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    session = get_session()
    user = session.query(Users).get(int(user_id))
    session.close()
    return user

def init_extensions(app):
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    # 初始化其他扩展...


