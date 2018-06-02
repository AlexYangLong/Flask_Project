import os
from datetime import timedelta

# 配置DEBUG
DEBUG = True

SECRET_KEY = os.urandom(24)

# 配置数据库
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'root'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'test_flask'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)

# 配置session-cookie的存活时间，默认是浏览器关闭就过期，7天
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

SQLALCHEMY_TRACK_MODIFICATIONS = False