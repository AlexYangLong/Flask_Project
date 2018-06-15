from flask_debugtoolbar import DebugToolbarExtension
from flask_restful import Api
from flask_session import Session
# from flask_sqlalchemy import SQLAlchemy

from bms.models import db

# 创建第三方包的对象
se = Session()
toolbar = DebugToolbarExtension()
api = Api()
# db = SQLAlchemy()  # 注意：在这里创建db对象会造成数据表创建不成功，应该在models中创建db，在这里引入


def init_exts(app):
    """初始化第三方包"""

    se.init_app(app=app)
    # toolbar.init_app(app=app)
    api.init_app(app=app)
    db.init_app(app=app)
