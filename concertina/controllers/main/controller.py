from flask import render_template, Blueprint
from concertina.app import cursor


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/homepage')
def homepage():

    cursor.execute("SELECT * FROM getConcertsByDate() NATURAL JOIN PLACES")
    incoming = cursor.fetchall()

    return render_template('concerts.html', incoming=incoming)
