import time
import os
from itsdangerous import JSONWebSignatureSerializer as Serializer
from flask import current_app, json, request

from .bp import admin_bp, allowed_file, secure_filename, CH_REGEX
from models import Admin
from utils import success, fail
from ext import cache


def generate_token(user_id):
    serializer = Serializer(current_app.config['SECRET_KEY'])
    return serializer.dumps({'user_id': user_id})


def verify_token(token):
    """
    解析出token以后看看redis里有没有，没有则需要再次登录，有则延长token在redis中的有效期
    :param token:  str
    :return:  解析出的dict if true else return False
    """
    serializer = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = serializer.loads(token)
    except:
        return False
    if 'user_id' in data and cache.get(data['user_id']):
        cache.expire(data['user_id'], current_app.config['EXPIRE_TIME'])
        return data
    return False


@admin_bp.route('/login', methods=['POST'])
def login():
    """帐密登录
    ---
    tags:
    - 登录
    parameters:
    - in: body
      name: body
      required: true
      schema:
        $ref: '#/parameters/user_login'
    responses:
      200:
        examples:
          code: 0
          data: {'token': 'abcdefgh'}
          message: 'success'
      401:
        examples:
          code: 1
          message: 'fail'
    # 登录验证成功后生成一个token存在redis中，设置了有效期，并返回
    # :return: Flask Response
    """
    try:
        data = json.loads(request.data)
    except:
        return fail(401)
    user = Admin.query.filter_by(username=data['username']).first()
    if user and user.verify_password(data['password']):
        token = generate_token(user.id).decode()
        res = {'data':
                   {'token': token}}
        cache.set(user.id, token)
        cache.expire(user.id, current_app.config['EXPIRE_TIME'])
        return success(res)
    return fail(401)


@admin_bp.route('/logout', methods=['POST'])
def logout():
    """登出
    ---
    tags:
    - 登录
    parameters:
    - in: body
      name: body
      required: true
      schema:
        $ref: '#/parameters/user_login'
    responses:
      200:
        examples:
          code: 0
          data: {'token': 'abcdefgh'}
          message: 'success'
      401:
        examples:
          code: 1
          message: 'fail'
    """
    data = verify_token(request.headers['Authorization'])
    cache.delete(data['user_id'])
    print(11)
    return success()


@admin_bp.route('/info')
def info():
    """获取用户信息
    ---
    tags:
    - 用户
    responses:
      200:
        description: 获取成功
        schema:
          type: object
          properties:
            code:
                type: int
            data:
                type: array
                $ref: '#/definitions/Module'
            message:
                type: string
        examples:
          code: 0
          data: [{}, {}]
          message: 'success'
    """
    token = request.args.get('token')
    data = verify_token(token)
    if not data:
        return fail(401)
    user = Admin.query.get_or_404(data['user_id'])
    if not user:
        return fail(401)
    res = {
        'data': {
            'name': user.name,
            'avatar': user.avatar
        }
    }
    return success(res)


@admin_bp.route('/user')
def users():
    """获取用户列表
    ---
    tags:
    - 用户
    security:
    - api_key: []
    responses:
      200:
        description: 获取成功
        schema:
          type: object
          properties:
            code:
                type: int
            data:
                type: array
                $ref: '#/definitions/Module'
            message:
                type: string
        examples:
          code: 0
          data: [{}, {}]
          message: 'success'
    """
    current_page = request.args.get('page') or 1
    per_page = request.args.get('limit') or 10
    pagination = Admin.query.paginate(int(current_page), per_page=int(per_page))
    result = [item.to_json() for item in pagination.items]
    res = {
        'data': {
            'items': result,
            'total': pagination.total
        }
    }
    return success(res)


@admin_bp.route('/user/<int:id>')
def get_user(id):
    """获取单个用户
    ---
    tags:
    - 用户
    security:
    - api_key: []
    responses:
      200:
        description: 获取成功
        schema:
          type: object
          properties:
            code:
                type: int
            data:
                type: array
                $ref: '#/definitions/Module'
            message:
                type: string
        examples:
          code: 0
          data: [{}, {}]
          message: 'success'
    """
    user = Admin.query.get_or_404(id)
    res = {
        'data': user.to_json()
    }
    return success(res)


@admin_bp.route('/user/create', methods=['POST'])
def create_user():
    """创建用户
    ---
    tags:
    - 用户
    security:
    - api_key: []
    responses:
      200:
        description: 获取成功
        schema:
          type: object
          properties:
            code:
                type: int
            data:
                type: array
                $ref: '#/definitions/Module'
            message:
                type: string
        examples:
          code: 0
          data: [{}, {}]
          message: 'success'
    """
    data = json.loads(request.data)
    Admin.create(**data)
    return success()


@admin_bp.route('/user/edit/<int:id>', methods=['PUT'])
def edit_user(id):
    """编辑用户
    ---
    tags:
    - 用户
    security:
    - api_key: []
    responses:
      200:
        description: 获取成功
        schema:
          type: object
          properties:
            code:
                type: int
            data:
                type: array
                $ref: '#/definitions/Module'
            message:
                type: string
        examples:
          code: 0
          data: [{}, {}]
          message: 'success'
    """
    data = json.loads(request.data)
    user = Admin.query.get_or_404(id)
    data['username'] = user.username
    if not data['password']:
        del data['password']
    user.update(**data)
    return success()


@admin_bp.route('/user/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    """删除用户
    ---
    tags:
    - 用户
    security:
    - api_key: []
    responses:
      200:
        description: 获取成功
        schema:
          type: object
          properties:
            code:
                type: int
            data:
                type: array
                $ref: '#/definitions/Module'
            message:
                type: string
        examples:
          code: 0
          data: [{}, {}]
          message: 'success'
    """
    user = Admin.query.get_or_404(id)
    if user:
        user.delete()
        return success()
    return fail(400)


@admin_bp.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    """上传头像
    ---
    tags:
    - 用户
    security:
    - api_key: []
    responses:
      200:
        description: 获取成功
        schema:
          type: object
          properties:
            code:
                type: int
            data:
                type: array
                $ref: '#/definitions/Module'
            message:
                type: string
        examples:
          code: 0
          data: [{}, {}]
          message: 'success'
    """
    file = request.files['avatar']
    if file:
        now = time.time()
        filename = str(int(now)) + file.filename
        if not allowed_file(filename):
            return fail(415)
        if not CH_REGEX.search(filename):
            filename = secure_filename(filename)
        UPLOAD_PATH = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatar')
        filepath = os.path.join(UPLOAD_PATH, filename)
        file.save(filepath)

        res = {'data':
            {
                'filename': filename,
                'fileurl': filepath
            }
        }
        return success(res)
    return fail(400)
