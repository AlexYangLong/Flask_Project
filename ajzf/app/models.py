from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class BaseModel(object):
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def add_update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(BaseModel, db.Model):
    __tablename__ = 't_user'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    phone = db.Column(db.String(12), unique=True, nullable=False)
    pwd_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(30), unique=True, nullable=False)
    avatar = db.Column(db.String(100))  # 头像
    id_name = db.Column(db.String(30))  # 身份证姓名
    id_card = db.Column(db.String(18), unique=True)  # 身份证ID

    # houses = db.relationship('House', backref='user')
    # orders = db.relationship('Order', backref='user')

    @property
    def password(self):
        return ''

    @password.setter
    def password(self, pwd):
        self.pwd_hash = generate_password_hash(pwd)

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd_hash, pwd)

    def to_auth_dict(self):
        return {
            'id_name': self.id_name,
            'id_card': self.id_card
        }

    def to_basic_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'avatar': self.avatar
        }
