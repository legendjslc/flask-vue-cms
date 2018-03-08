from ext import db

from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


class BaseModel(db.Model):

    __abstract__ = True

    id = db.Column('id', db.Integer, primary_key=True)
    _created_at = db.Column('created_at', db.DateTime, default=datetime.now)
    _updated_at = db.Column('updated_at', db.DateTime, default=datetime.now, onupdate=datetime.now)
    default_json_fields = []

    @hybrid_property
    def updated_at(self):
        return self._updated_at.strftime('%Y-%m-%d %H:%M:%S') if self._updated_at else None

    @hybrid_property
    def created_at(self):
        return self._created_at.strftime('%Y-%m-%d %H:%M:%S')

    def to_json(self, child_num=None, fields=None):
        """
        将模型中的json_fields字段转化为JSON显示，判断如果是一对多关系显示子模型中的json_fields
        :param child_num: int
        :param json_fields: list
        :return: dict
        """
        res = {}
        json_fields = self.default_json_fields if not fields else fields
        for k in json_fields:
            if k in self.__mapper__.relationships.keys():
                res[k] = []
                for c in getattr(self, k)[:child_num]:
                    res[k].append(c.to_json())
            else:
                res[k] = getattr(self, k)
        return res

    @classmethod
    def get(cls, num=None, child_num=None):
        """
        :param num: int or str('all')
        :param child_num: int
        :return: dict
        """
        items = cls.get_item(num)
        return [item.to_json(child_num) for item in items]

    @classmethod
    def get_item(cls, num=None):
        """
        执行模型查询，有排序字段时加入排序字段进行查询
        :param num: int or str('all'), if None means 1
        :return: list
        """
        if hasattr(cls, 'order'):
            order = 'order'
        else:
            order = 'updated_at'

        if num is 'all':
            items = cls.query.order_by(order).all()
            return items
        elif num is None:
            num = 1
        items = cls.query.order_by(order)[:num]
        return items


class Article(BaseModel):
    __tablename__ = 'articles'
    title = db.Column('title', db.String)
    content = db.Column('content', db.Text)
    thumb_pic = db.Column('thumb_pic', db.String)
    order = db.Column('order', db.Integer)
    module_id = db.Column('module_id', db.Integer, db.ForeignKey('modules.id'))

    default_json_fields = ['title', 'order', 'id', 'thumb_pic', 'summary', 'updated_at', 'module_name', 'module_id']

    @hybrid_property
    def summary(self):
        return self.content[:100]

    @hybrid_property
    def module_name(self):
        if self.module:
            return str(self.module)
        return ''


class Module(BaseModel):
    __tablename__ = 'modules'
    order = db.Column('order', db.Integer)
    title = db.Column('title', db.String)
    template_id = db.Column('template_id', db.Integer)
    child = db.relationship('Article', backref='module', lazy='dynamic')
    default_json_fields = ['order', 'template_id', 'id', 'child', 'title']

    def __repr__(self):
        return self.title


class Admin(BaseModel):
    __tablename__ = 'admin_users'
    username = db.Column('username', db.String)
    password = db.Column('password', db.String)
    name = db.Column('name', db.String)
    avatar = db.Column('avatar', db.String)
    operations = db.relationship('OperationLog', backref='admin', lazy='dynamic')
    default_json_fields = ['id', 'username', 'name', 'avatar', 'updated_at']

    def generate_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class OperationLog(BaseModel):
    __tablename__ = 'admin_operation_log'
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('admin_users.id'))
    path = db.Column('path', db.String)
    method = db.Column('method', db.String(15))
    ip = db.Column('ip', db.String(15))
    input = db.Column('input', db.JSON)
