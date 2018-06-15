import os

import redis


class CommonConfig(object):
    pass


class DevConfig(CommonConfig):

    # 配置Debug模式为 True
    DEBUG = True

    SECRET_KEY = os.urandom(24)
    # session相关配置，并将session中的数据保存到redis
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port='6379')

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
            'mysql', 'pymysql', 'root', 'root', '127.0.0.1', '3306', 'bms')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
