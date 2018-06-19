SUCCESS = {'code': 200, 'msg': '操作成功'}

# 用户模块
PARAMS_NOT_COMPLETE = {'code': 1001, 'msg': '请求参数不完整'}
USER_NOT_EXISTS = {'code': 1002, 'msg': '用户名不存在'}
USER_PASSWORD_ERROR = {'code': 1003, 'msg': '密码错误'}
USER_USERNAME_OR_PASSWORD_ERROR = {'code': 1004, 'msg': '用户名或密码错误'}

# 权限模块
AUTHORITY_PARAMS_ERROR = {'code': 1101, 'msg': '参数错误'}
AUTHORITY_NOT_EXISTS = {'code': 1102, 'msg': '该权限不存在'}
AUTHORITY_EXISTED = {'code': 1103, 'msg': '该权限名已存在'}
