SUCCESS = {'code': 200, 'msg': '操作成功'}
DATABASE_ERROR = {'code': 0, 'msg': '数据库错误，请稍后重试'}

# 用户模块
USER_PARAMS_NOT_COMPLETE = {'code': 1001, 'msg': '请求参数不完整'}
USER_PHONE_ERROR = {'code': 1002, 'msg': '手机号码格式错误'}
USER_TWICE_PASSWORD_DIFFERENT = {'code': 1003, 'msg': '两次密码不一致'}
USER_PHONE_REGISTERED = {'code': 1004, 'msg': '手机号已被注册'}
USER_USERNAME_EXISTED = {'code': 1005, 'msg': '用户名已存在'}

USER_NOT_EXISTS = {'code': 1006, 'msg': '用户名不存在'}
USER_PASSWORD_ERROR = {'code': 1007, 'msg': '密码错误'}

USER_IMAGE_FORMAT_ERROR = {'code': 1008, 'msg': '上传图片格式不正确'}

USER_AUTH_DATA_NOT_NULL = {'code': 1009, 'msg': '实名认证信息不能为空'}
USER_AUTH_IDCARD_INVALID = {'code': 1010, 'msg': '身份证号格式错误'}

# 房源
HOUSE_PARAMS_NOT_COMPLETE = {'code': 1101, 'msg': '请求参数不完整'}

# 订单
ORDER_PARAMS_NOT_COMPLETE = {'code': 1201, 'msg': '请求参数不完整'}
ORDER_TIME_PARAMS_ERROR = {'code': 1202, 'msg': '时间参数错误'}
