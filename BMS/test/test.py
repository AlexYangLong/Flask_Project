from flask import Blueprint

test_blueprint = Blueprint('test', __name__)

@test_blueprint.route('/test/')
def test():
    return 'test'