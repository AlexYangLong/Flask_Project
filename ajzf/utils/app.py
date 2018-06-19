import os
from flask import Flask

from app.user.user_views import user_blueprint
from utils.common import BASE_DIR
from utils.config import DevConfig
from utils.exts import init_exts


def create_app():
    # 获取static、templates路径
    templates_dir = os.path.join(BASE_DIR, 'templates')
    static_dir = os.path.join(BASE_DIR, 'static')

    # 创建实例app
    app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)

    # 加载配置文件
    app.config.from_object(DevConfig)

    # 测试配置是否成功
    # @app.route('/test/')
    # def test():
    #     return 'hello'

    # 使用自定义方法集中初始化第三方包
    init_exts(app=app)

    # 注册蓝图
    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app
