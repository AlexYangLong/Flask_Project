from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(object):
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
    create_time = db.Column(db.DateTime, default=datetime.now)

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
            'role': Role.query.get(self.role_id).name
        }


class Authority(BaseModel, db.Model):
    __tablename__ = 'authority'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
        }


role_auth = db.Table('role_auth',
                     db.Column('id',db.Integer, primary_key=True, autoincrement=True),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'), nullable=False),
                     db.Column('auth_id', db.Integer, db.ForeignKey('authority.id'),nullable=False)
                     )


class Role(BaseModel, db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    admins = db.relationship('Admin', backref='role', lazy=True)

    authorities = db.relationship('Authority', secondary=role_auth, backref='roles', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time.strftime('%Y-%m-%d %X')
        }


class Student(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.Boolean, nullable=False, default=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'create_time': self.create_time.strftime('%Y-%m-%d %X'),
            'grade_id': self.grade_id
        }


class Grade(BaseModel, db.Model):
    __tablename__ = 'grade'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    students = db.relationship('Student', backref='grade', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time.strftime('%Y-%m-%d %X'),
            'students': [stu.to_dict() for stu in self.students]
        }
