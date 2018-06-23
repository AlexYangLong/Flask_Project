import os

import redis


class CommonConfig(object):

    # 配置session
    SECRET_KEY = os.urandom(24)


class DevConfig(CommonConfig):
    DEBUG = True

    # 将session中的数据保存到redis
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port='6379', password='yl@952001')

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        'mysql', 'pymysql', 'root', 'root', '127.0.0.1', '3306', 'ajzf')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProConfig(CommonConfig):
    DEBUG = False
