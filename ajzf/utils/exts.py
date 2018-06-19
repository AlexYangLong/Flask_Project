from flask_session import Session
from flask_restful import Api

from app.models import db

# 创建第三方包的对象
se = Session()
api = Api()


def init_exts(app):
    """使用app初始化"""

    se.init_app(app=app)
    api.init_app(app=app)
    db.init_app(app=app)
