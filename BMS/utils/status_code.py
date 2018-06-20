SUCCESS = {'code': 200, 'msg': '操作成功'}

PARAMS_NOT_COMPLETE = {'code': 500, 'msg': '请求参数不完整，参数错误'}

# 用户模块
USER_NOT_EXISTS = {'code': 1001, 'msg': '用户名不存在'}
USER_PASSWORD_ERROR = {'code': 1002, 'msg': '密码错误'}
USER_USERNAME_OR_PASSWORD_ERROR = {'code': 1003, 'msg': '用户名或密码错误'}
USER_USERNAME_EXISTED = {'code': 1004, 'msg': '用户名已存在'}
USER_TWICE_PASSWORD_DIFFERENT = {'code': 1005, 'msg': '两次密码不一致'}
USER_OLD_PASSWORD_ERROR = {'code': 1006, 'msg': '原密码错误'}

# 权限模块
AUTHORITY_NOT_EXISTS = {'code': 1101, 'msg': '该权限不存在'}
AUTHORITY_EXISTED = {'code': 1102, 'msg': '该权限名已存在'}

# 角色模块
ROLE_NOT_EXISTS = {'code': 1201, 'msg': '该角色不存在'}
ROLE_EXISTED = {'code': 1202, 'msg': '该角色已存在'}

# 班级模块
GRADE_NOT_EXISTS = {'code': 1301, 'msg': '该班级不存在'}
GRADE_EXISTED = {'code': 1302, 'msg': '该班级已存在'}

# 学生模块
STUDENT_NOT_EXISTS = {'code': 1401, 'msg': '该学生不存在'}
STUDENT_EXISTED = {'code': 1402, 'msg': '该学生已存在'}
