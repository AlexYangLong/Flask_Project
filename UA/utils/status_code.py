SUCCESS = {'code': 200, 'msg': '操作成功'}

DATABASE_ERROR = {'code': 500, 'msg': '操作数据库失败'}

ERROR_CODE = 400
SUCCESS_CODE = 200

# 登录
ADMIN_NOT_EXISTS = {'code': 1101, 'msg': '登录用户不存在'}
ADMIN_AUTH_PASSWORD_ERROR = {'code': 1102, 'msg': '密码认证失败'}
ADMIN_LOGIN_RECORD_INSERT_ERROR = {'code': 1103, 'msg': '创建登录记录失败'}
ADMIN_ACCOUNT_DELETED = {'code': 1104, 'msg': '管理员账户已被删除'}
ADMIN_PHONE_EXISTS = {'code': 1105, 'msg': '电话号码已存在'}
ADMIN_NOT_LOGINED = {'code': 1106, 'msg': '未登录'}
ADMIN_AUTHORITY_ERROR = {'code': 1107, 'msg': '权限错误'}

# 用户
USER_NOT_EXISTS = {'code': 1201, 'msg': '用户不存在'}
USER_PHONE_EXISTS = {'code': 1202, 'msg': '电话号码已存在'}
USER_DELETED = {'code': 1203, 'msg': '用户已被删除'}

# 预约
APPOINT_NOT_EXISTS = {'code': 1301, 'msg': '预约单不存在'}
APPOINT_DELETED = {'code': 1302, 'msg': '预约单已被删除'}

