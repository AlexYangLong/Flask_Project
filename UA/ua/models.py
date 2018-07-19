from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class BaseModel(object):
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_delete = db.Column(db.Boolean, default=False)
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    def add_update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        self.is_delete = True
        db.session.add(self)
        db.session.commit()


class Admin(BaseModel, db.Model):
    __tablename__ = 'admin'
    username = db.Column(db.String(20), nullable=False)
    pwd_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(64))
    avatar = db.Column(db.String(200))

    login_records = db.relationship('LoginRecord', backref='admin')
    appointments = db.relationship('Appointment', backref='admin')
    users = db.relationship('User', backref='admin')

    @property
    def password(self):
        return ''

    @password.setter
    def password(self, pwd):
        self.pwd_hash = generate_password_hash(pwd)

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd_hash, pwd)

    def to_basic_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'phone': self.phone,
            'email': self.email if self.email else '',
            'avatar': self.avatar if self.avatar else '',
            'create_time': self.create_time.strftime('%Y-%m-%d %X'),
            'update_time': self.update_time.strftime('%Y-%m-%d %X'),
            'is_delete': self.is_delete
        }

    def to_appointment_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'phone': self.phone,
            'email': self.email if self.email else '',
            'avatar': self.avatar if self.avatar else '',
            'create_time': self.create_time.strftime('%Y-%m-%d %X'),
            'update_time': self.update_time.strftime('%Y-%m-%d %X'),
            'is_delete': self.is_delete,
            'appointments': [a.to_admin_dict() for a in self.appointments]
        }

    def to_login_record_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'phone': self.phone,
            'email': self.email if self.email else '',
            'avatar': self.avatar if self.avatar else '',
            'create_time': self.create_time.strftime('%Y-%m-%d %X'),
            'update_time': self.update_time.strftime('%Y-%m-%d %X'),
            'is_delete': self.is_delete,
            'login_records': [lr.to_admin_dict() for lr in self.login_records]
        }

    def to_user_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'phone': self.phone,
            'email': self.email if self.email else '',
            'avatar': self.avatar if self.avatar else '',
            'create_time': self.create_time.strftime('%Y-%m-%d %X'),
            'update_time': self.update_time.strftime('%Y-%m-%d %X'),
            'is_delete': self.is_delete,
            'users': [user.to_basic_dict() for user in self.users]
        }

    def to_full_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'phone': self.phone,
            'email': self.email if self.email else '',
            'avatar': self.avatar if self.avatar else '',
            'create_time': self.create_time.strftime('%Y-%m-%d %X'),
            'update_time': self.update_time.strftime('%Y-%m-%d %X'),
            'is_delete': self.is_delete,
            'appointments': [a.to_admin_dict() for a in self.appointments],
            'login_records': [lr.to_admin_dict() for lr in self.login_records]
        }


class LoginRecord(BaseModel, db.Model):
    login_time = db.Column(db.DateTime, default=datetime.now)
    login_ip = db.Column(db.String(20), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    def to_basic_dict(self):
        return {
            'id': self.id,
            'login_time': self.login_time.strftime('%Y-%m-%d %X'),
            'login_ip': self.login_ip,
            'login_admin': self.admin.to_basic_dict(),
            'create_time': self.create_time.strftime('%Y-%m-%d %X'),
            'update_time': self.update_time.strftime('%Y-%m-%d %X'),
            'is_delete': self.is_delete
        }

    def to_admin_dict(self):
        return {
            'id': self.id,
            'login_time': self.login_time.strftime('%Y-%m-%d %X'),
            'login_ip': self.login_ip,
            'create_time': self.create_time.strftime('%Y-%m-%d %X'),
            'update_time': self.update_time.strftime('%Y-%m-%d %X'),
            'is_delete': self.is_delete
        }


class User(BaseModel, db.Model):
    __tablename__ = 'user'
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(64))
    address = db.Column(db.String(200))
    reason = db.Column(db.String(400))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    appointments = db.relationship('Appointment', backref='user')

    def to_basic_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email if self.email else '',
            'address': self.address if self.address else '',
            'reason': self.reason if self.reason else '',
            'create_time': self.create_time.strftime('%Y-%m-%d %X'),
            'update_time': self.update_time.strftime('%Y-%m-%d %X'),
            'is_delete': self.is_delete
        }

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email if self.email else '',
            'address': self.address if self.address else '',
            'reason': self.reason if self.reason else '',
            'admin': self.admin.to_basic_dict(),
            'create_time': self.create_time.strftime('%Y-%m-%d %X'),
            'update_time': self.update_time.strftime('%Y-%m-%d %X'),
            'is_delete': self.is_delete
        }

    def to_full_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email if self.email else '',
            'address': self.address if self.address else '',
            'reason': self.reason if self.reason else '',
            'admin': self.admin.to_basic_dict(),
            'create_time': self.create_time.strftime('%Y-%m-%d %X'),
            'update_time': self.update_time.strftime('%Y-%m-%d %X'),
            'is_delete': self.is_delete,
            'appointments': [a.to_user_dict() for a in self.appointments]
        }


class Appointment(BaseModel, db.Model):
    __tablename__ = 'appointment'
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    def to_admin_dict(self):
        return {
            'id': self.id,
            'create_time': self.create_time.strftime('%Y-%m-%d %X'),
            'update_time': self.update_time.strftime('%Y-%m-%d %X'),
            'is_delete': self.is_delete,
            'start_time': self.start_time.strftime('%Y-%m-%d %X'),
            'end_time': self.end_time.strftime('%Y-%m-%d %X'),
            'user': self.user.to_basic_dict()
        }

    def to_user_dict(self):
        return {
            'id': self.id,
            'create_time': self.create_time.strftime('%Y-%m-%d %X'),
            'update_time': self.update_time.strftime('%Y-%m-%d %X'),
            'is_delete': self.is_delete,
            'start_time': self.start_time.strftime('%Y-%m-%d %X'),
            'end_time': self.end_time.strftime('%Y-%m-%d %X'),
            'admin': self.admin.to_basic_dict()
        }

    def to_full_dict(self):
        return {
            'id': self.id,
            'create_time': self.create_time.strftime('%Y-%m-%d %X'),
            'update_time': self.update_time.strftime('%Y-%m-%d %X'),
            'is_delete': self.is_delete,
            'start_time': self.start_time.strftime('%Y-%m-%d %X'),
            'end_time': self.end_time.strftime('%Y-%m-%d %X'),
            'admin': self.admin.to_basic_dict(),
            'user': self.user.to_basic_dict()
        }
