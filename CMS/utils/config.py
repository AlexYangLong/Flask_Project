import os
from datetime import timedelta

import redis


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Common(object):
    pass


class DevConfig(Common):
    DEBUG = True

    # SECRET_KEY = os.urandom(24)
    SECRET_KEY = '123456789!@#$%^&*()qwertyuiopasdfghjklzxcvbnm'
    SESSION_TYPE = 'filesystem'
    # 配置session-cookie的存活时间，默认是浏览器关闭就过期，7天
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # session相关配置，并将session中的数据保存到redis
    # SESSION_TYPE = 'redis'
    # SESSION_REDIS = redis.Redis(host='127.0.0.1', port='6379')

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        'mysql', 'pymysql', 'root', 'root', '127.0.0.1', '3306', 'cms')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProConfig(Common):
    DEBUG = False
