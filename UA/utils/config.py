import os
from datetime import timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))


class CommonConfig(object):
    pass


class DevelopConfig(CommonConfig):
    DEBUG = True

    SECRET_KEY = '123456789!@#$%^&*()qwertyuiopasdfghjklzxcvbnm'
    SESSION_TYPE = 'filesystem'
    # 配置session-cookie的存活时间，默认是浏览器关闭就过期，7天
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        'mysql', 'pymysql', 'root', 'root', '127.0.0.1', '3306', 'ua')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductConfig(CommonConfig):
    DEBUG = False