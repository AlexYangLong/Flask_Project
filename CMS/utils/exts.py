from flask_session import Session
from flask_restful import Api

from cms.models import db

# 创建第三方库实例
se = Session()
api = Api()


def init_exts(app):
    """
    自定义初始化第三方库
    :param app: 程序实例app
    :return:
    """
    se.init_app(app=app)
    api.init_app(app=app)
    db.init_app(app=app)
