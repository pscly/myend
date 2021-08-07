
from flask import Blueprint

bp = Blueprint('/', __name__)


# /
@bp.route('/', methods=['GET'])
def index():
    return '你好，这里是根节点，你为什么会来这里呢？我很好奇，你不该来这个网站的'

# /robot.txt
@bp.route('/robot.txt', methods=['GET'])
def robot():
    return 'User-agent: *\nDisallow: /'

