from flask import render_template, Blueprint

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/homepage')
def homepage():
    return render_template('concerts.html')
