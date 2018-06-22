---
爱家租房 —— 接口文档
---
#用户模块
##1、注册
###1.1、注册页面
请求：
```
GET     /user/register/
```
响应：register.html页面
###1.2、用户注册
请求：
```
POST    /user/register/
```
响应：
```
错误1：
{'code': 1001, 'msg': '请求参数不完整'}
错误2：
{'code': 1002, 'msg': '手机号码格式错误'}
错误3：
{'code': 1003, 'msg': '两次密码不一致'}
错误4：
{'code': 1004, 'msg': '手机号已被注册'}
错误5：
{'code': 1005, 'msg': '用户名已存在'}

正确：
{'code': 200, 'msg': '操作成功'}
```
参数：
```
{
    'phone': 手机号,
    'username': 用户名,
    'password': 密码,
    'password2': 确认密码
}
```
##2、登录
###2.1、登录页面
请求：
```
GET     /user/login/
```
响应：login.html页面
###2.2、用户登录
请求：
```
POST    /user/login/
```
响应：
```
错误1：
{'code': 1001, 'msg': '请求参数不完整'}
错误2：
{'code': 1006, 'msg': '用户名不存在'}
错误3：
{'code': 1007, 'msg': '密码错误'}
正确：
{'code': 200, 'msg': '操作成功'}
```
参数：
```
{
    'mobile': 用户名或手机号,
    'password': 密码
}
```
##3、注销
请求：
```
GET     /user/logout/
```
响应：重定向到 /user/login/
##4、个人中心
###4.1、个人中心页面
请求：
```
GET     /user/mine/
```
响应：my.html页面
###4.2、修改个人信息页面
请求：
```
GET     /user/profile/
```
响应：profile.html页面
###4.3、获取用户名与头像
请求：
```
GET     /user/get_name_img/
```
响应：
```
错误：
{'code': 0, 'msg': '数据库错误，请稍后重试'}
正确：
{
    'code': 200,
    'msg': '操作成功',
    'data': 
    {
        'id': 用户id,
        'name': 用户名,
        'phone': 用户手机号,
        'avatar': 用户头像
    }
}
```
###4.4、上传头像
请求：
```
PATCH       /user/avatar/
```
响应：
```
错误1：
{'code': 1008, 'msg': '上传图片格式不正确'}
错误2：
{'code': 0, 'msg': '数据库错误，请稍后重试'}
正确：
{
    'code': 200,
    'msg': '操作成功',
    'user_id': 用户id,
    'img_url': 图片保存后的路径
}
```
参数：
```
{
    'file': 图片
}
```
###4.5、修改用户名
请求：
```
PATCH       /user/username/
```
响应：
```
错误1：
{'code': 1001, 'msg': '请求参数不完整'}
错误2：
{'code': 1005, 'msg': '用户名已存在'}
错误3：
{'code': 0, 'msg': '数据库错误，请稍后重试'}
正确：
{'code': 200, 'msg': '操作成功'}
```
参数：
```
{
    'username': 新用户名
}
```
###4.6、认证界面
请求：
```
GET     /user/authenticate/
```
响应：auth.html页面
###4.7、用户认证
请求：
```
PATCH       /user/authenticate/
```
响应：
```
错误1：
{'code': 1009, 'msg': '实名认证信息不能为空'}
错误2：
{'code': 1010, 'msg': '身份证号格式错误'}
错误3：
{'code': 0, 'msg': '数据库错误，请稍后重试'}
正确：
{'code': 200, 'msg': '操作成功'}
```
参数：
```
{
    'real_name': 姓名,
    'id_card': 身份证号
}
```
###4.8、获取认证信息
请求：
```
GET     /user/auth_info/
```
响应：
```
错误：
{'code': 0, 'msg': '数据库错误，请稍后重试'}
正确：
{
    'code': 200,
    'msg': '操作成功',
    'data': 
    {
        'id_name': 姓名,
        'id_card': 身份证号
    }
}
```
#房屋模块
##1、我的房源
请求：
```
GET     /house/my_house/
```
响应：myhouse.html页面
##2、发布房源页面
请求：
```
GET     /house/new_house/
```
响应：newhouse.html页面
##3、获取区域和设备信息
请求：
```
GET     /house/area_facility/
```
响应：
```
正确：
{
    'code': 200,
    'msg': '操作成功',
    'area_list': [{
        'id': 区域id,
        'name': 区域名
    }],
    'facility_list': [{
        'id': 设备id,
        'name': 设备名,
        'css': 设备图标
    }]
}
```
##4、获取我的房源列表
请求：
```
GET     /house/house_list/
```
响应：
```
错误：
{'code': 0, 'msg': '数据库错误，请稍后重试'}
正确：
{
    'code': 200,
    'msg': '操作成功',
    'data_list': [{
        'id': 房源id,
        'title': 房源标题,
        'image': 房源封面,
        'area': 所在区域,
        'price': 单价,
        'create_time': 发布时间,       
        'room_count': 房间数量,
        'order_count': 被订数量,
        'address': 详细地址
    }]
}
```
##5、发布房源
请求：
```
POST        /house/publish_house/
```
响应：
```
错误1：
{'code': 1101, 'msg': '请求参数不完整'}
错误2：
{'code': 0, 'msg': '数据库错误，请稍后重试'}
正确：
{
    'code': 200,
    'msg': '操作成功',
    'data': {
        'id': 房源id,
        'title': 房源标题,
        'image': 房源封面,
        'area': 所在区域,
        'price': 单价,
        'create_time': 发布时间,       
        'room_count': 房间数量,
        'order_count': 被订数量,
        'address': 详细地址
    }
}
```
参数：
```
{
    'title': 房源标题,
    'price': 单间,
    'area_id': 区域id,
    'address': 详细地址,
    'room_count': 房间数量,
    'acreage': 房间面积,
    'unit': 房源规格,
    'capacity': 可容纳人数,
    'beds': 床规格,
    'deposit': 收取押金,
    'min_days': 最少入住天数,
    'max_days': 最多入住天数,
    'check_val': 设备ids的字符串
}
```
##6、上传房源的图片
请求：
```
POST        /house/upload_image/
```
响应：
```
错误：
{'code': 0, 'msg': '数据库错误，请稍后重试'}
正确：
{'code': 200, 'msg': '操作成功'}
```
参数：
```
{
    'hid': 房源id,
    'house_image': [], 图片列表
}
```
##7、房源详情页面
请求：
```
GET     /house/house_detail/
```
响应：detail.html页面
##8、获取房源详情
请求：
```
GET     /house/house_info/<int:hid>/    hid：房源id
```
响应：
```
错误1：
{'code': 1101, 'msg': '请求参数不完整'}
错误2：
{'code': 0, 'msg': '数据库错误，请稍后重试'}
正确：
{
    'code': 200,
    'msg': '操作成功',
    'data': {
        'id': 房源id,
        'user_avatar': 房主头像,
        'user_name': 房主用户名,
        'title': 房源标题,
        'price': 单价,
        'address': 详细地址,
        'room_count': 房间数量,
        'acreage': 房间面积,
        'unit': 房源规格,
        'capacity': 可容纳人数,
        'beds': 床规格,
        'deposit': 收取押金,
        'min_days': 最少入住天数,
        'max_days': 最多入住天数,
        'order_count': 被订数量,
        'images': [], 房源图片列表
        'facilities': [{
            'id': 设备id,
            'name': 设备名,
            'css': 设备图标
        }], 房源设备列表
    },
    'comments': [{
        'order_id': 订单id,
        'user_name': 订单所属用户名,
        'house_title': 房源标题,
        'image': 房源封面,
        'create_date': 发布时间,
        'begin_date': 开始入住日期,
        'end_date': 退房日期,
        'amount': 总价,
        'days': 入住天数,
        'status': 订单状态,
        'comment': 评论
    }] 订单评论列表
}
```
#订单模块
##1、预订页面
请求：
```
GET     /book/booking/
```
响应：booking.html页面
##2、预订房间
请求：
```
POST    /book/check_in/
```
响应：
```
错误1：
{'code': 1201, 'msg': '请求参数不完整'}
错误2：
{'code': 1202, 'msg': '时间参数错误'}
错误3：
{'code': 0, 'msg': '数据库错误，请稍后重试'}
正确：
{'code': 200, 'msg': '操作成功'}
```
参数：
```
{
    'hid': 房源id,
    'begin': 开始入住日期,
    'end': 退房日期,
    'days': 总天数,
    'price': 单价,
    'amount': 总价
}
```