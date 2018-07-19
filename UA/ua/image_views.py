import random
import re

import os
from flask import Blueprint, request, render_template, jsonify

from utils.config import ROOT_DIR

img_blueprint = Blueprint('img', __name__)


@img_blueprint.route('/img/', methods=['GET', 'POST'])
def img():
    if request.method == 'GET':
        return render_template('test_img.html')
    elif request.method == 'POST':
        img_list = request.files.getlist('img')
        # 验证图片格式
        for file in img_list:
            if not re.match(r'image/.*', file.mimetype):
                return jsonify({'code': 400, 'msg': '上传图片格式不正确，png/jpg/gif'})

        # 保存
        file_dir = os.path.join(ROOT_DIR, 'static/upload')
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        path_list = []
        for file in img_list:
            file_name = str(random.randint(1, 10000)) + '.' + file.filename.split('.')[-1]
            img_path = os.path.join(file_dir, file_name)
            path_list.append('/static/upload/' + file_name)
            file.save(img_path)

        return jsonify({'code': 200, 'msg': '操作成功', 'img_list': path_list})
