from flask_session import Session
from flask_restful import Api

from ua.models import db

se = Session()
api = Api()


def init_exts(app):
    se.init_app(app=app)
    api.init_app(app=app)
    db.init_app(app=app)
