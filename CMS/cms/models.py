from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

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


class Admin(BaseModel, db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(256), nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)

    def __init__(self, username, name, password):
        self.username = username
        self.name = name
        self.password = password

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'password': self.password,
            'create_time': self.create_time.strftime('%Y-%m-%d %X'),
            'role_id': self.role_id,
            'role': self.role.name
        }


class Authority(BaseModel, db.Model):
    __tablename__ = 'authority'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(64))

    parent_id = db.Column(db.Integer, db.ForeignKey('authority.id'))

    # sub_authoritires = db.relationship('Authority', backref='parent', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'parent_id': self.parent_id,
            'parent': Authority.query.get(self.parent_id).name if self.parent_id else '',
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
        }

    def to_parent_info_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'sub_auths': [auth.to_dict() for auth in Authority.query.filter(Authority.parent_id == self.id)],
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
        }


role_auth = db.Table('role_auth',
                     db.Column('id',db.Integer, primary_key=True, autoincrement=True),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'), nullable=False),
                     db.Column('auth_id', db.Integer, db.ForeignKey('authority.id'), nullable=False)
                     )


class Role(BaseModel, db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(64))

    admins = db.relationship('Admin', backref='role', lazy=True)
    authorities = db.relationship('Authority', secondary=role_auth, backref='roles', lazy='dynamic')

    def to_base_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
        }

    def to_admins_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'admin_list': ','.join([admin.name for admin in self.admins]),
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
        }

    def to_auths_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            # 'authority_list': [auth.to_dict() for auth in self.authorities],
            'auths': ','.join([str(auth.id) for auth in self.authorities]),
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
        }

    def to_full_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'admin_list': [admin.to_dict() for admin in self.admins],
            'authority_list': [auth.to_dict() for auth in self.authorities],
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
        }
