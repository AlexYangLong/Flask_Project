from flask import Blueprint, render_template


chart_blueprint = Blueprint('chart', __name__)


@chart_blueprint.route('/chart-1/')
def chart_1():
    return render_template('chart/charts-1.html')
