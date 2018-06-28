import os
from flask import Flask

from cms.admin_views import admin_blueprint
from cms.auth_views import auth_blueprint
from cms.db_views import db_blueprint
from cms.index_views import index_blueprint
from utils.config import DevConfig, BASE_DIR
from utils.exts import init_exts


def create_app():
    # 获取templates、static目录的路径
    template_dir = os.path.join(BASE_DIR, 'templates')
    static_dir = os.path.join(BASE_DIR, 'static')

    # 创建程序实例
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # 加载配置
    app.config.from_object(DevConfig)

    # 使用自定义方法初始化第三方库
    init_exts(app=app)

    # 注册蓝图
    app.register_blueprint(blueprint=db_blueprint, url_prefix='/db')
    app.register_blueprint(blueprint=index_blueprint, url_prefix='/index')
    app.register_blueprint(blueprint=admin_blueprint, url_prefix='/admin')
    app.register_blueprint(blueprint=auth_blueprint, url_prefix='/auth')

    return app
