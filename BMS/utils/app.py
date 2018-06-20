import os
from flask import Flask

from bms.auth_views import auth_blueprint
from bms.authority_views import authority_blueprint
from bms.db_views import db_blueprint
from bms.grade_views import grade_blueprint
from bms.index_views import index_blueprint
from bms.role_views import role_blueprint
from bms.student_views import student_blueprint
from bms.user_views import user_blueprint
from test.test import test_blueprint
from utils.config import DevConfig
from utils.exts import init_exts


def create_app():
    """用于创建程序实例"""

    # 获取项目中templates、static的目录路径
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    templates_dir = os.path.join(BASE_DIR, 'templates')
    static_dir = os.path.join(BASE_DIR, 'static')

    # 创建程序实例app
    app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)

    # 加载配置信息
    app.config.from_object(DevConfig)

    # 使用自定义方法，初始化第三方包
    init_exts(app=app)

    # 注册蓝图
    app.register_blueprint(blueprint=test_blueprint, url_prefix='/test')
    app.register_blueprint(blueprint=db_blueprint, url_prefix='/db')
    app.register_blueprint(blueprint=auth_blueprint, url_prefix='/auth')
    app.register_blueprint(blueprint=index_blueprint, url_prefix='/index')
    app.register_blueprint(blueprint=authority_blueprint, url_prefix='/authority')
    app.register_blueprint(blueprint=role_blueprint, url_prefix='/role')
    app.register_blueprint(blueprint=grade_blueprint, url_prefix='/grade')
    app.register_blueprint(blueprint=student_blueprint, url_prefix='/student')
    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')

    return app
