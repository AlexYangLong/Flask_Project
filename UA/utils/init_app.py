import os
from flask import Flask

from ua.admin_views import admin_blueprint
from ua.appointment_views import appoint_blueprint
from ua.auth_views import auth_blueprint
from ua.chart_views import chart_blueprint
from ua.db_views import db_blueprint
from ua.image_views import img_blueprint
from ua.index_views import index_blueprint
from ua.user_views import user_blueprint
from utils.config import DevelopConfig, ROOT_DIR
from utils.exts import init_exts


def create_app():
    static_dir = os.path.join(ROOT_DIR, 'static')
    templates_dir = os.path.join(ROOT_DIR, 'templates')

    app = Flask(__name__, static_folder=static_dir, template_folder=templates_dir)

    # 加载配置项
    app.config.from_object(DevelopConfig)

    # 使用自定义方法初始化第三方库
    init_exts(app=app)

    # 注册蓝图
    app.register_blueprint(db_blueprint, url_prefix='/db')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(appoint_blueprint, url_prefix='/appoint')
    app.register_blueprint(index_blueprint, url_prefix='/index')

    app.register_blueprint(img_blueprint, url_prefix='/img')
    app.register_blueprint(chart_blueprint, url_prefix='/chart')

    return app
