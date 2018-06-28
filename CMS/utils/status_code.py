SUCCESS = {'code': 200, 'msg': '请求成功'}

PARAMS_NOT_COMPLETE = {'code': 501, 'msg': '请求参数不完整'}
DATABASE_ERROR = {'code': 502, 'msg': '数据库操作错误'}

# 权限
AUTHORITY_NOT_EXISTS = {'code': 1001, 'msg': '该权限不存在'}
AUTHORITY_ALREADY_EXISTS = {'code': 1002, 'msg': '该权限名已存在'}

# 角色
ROLE_NOT_EXISTS = {'code': 1101, 'msg': '该角色不存在'}
ROLE_ALREADY_EXISTS = {'code': 1102, 'msg': '该角色名已存在'}

# 管理员
ADMIN_NOT_EXISTS = {'code': 1201, 'msg': '该管理员不存在'}
ADMIN_ALREADY_EXISTS = {'code': 1202, 'msg': '该管理员登录名已存在'}

# 登录
LOGIN_AUTHENTICATE_FAILED = {'code': 503, 'msg': '认证失败，用户名或密码错误'}
