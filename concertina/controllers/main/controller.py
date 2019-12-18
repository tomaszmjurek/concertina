from flask import render_template, Blueprint
from concertina.app import cursor
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/homepage')
def homepage():

    cursor.execute("""SELECT * FROM concerts NATURAL JOIN PLACES
                        WHERE concert_date < CURRENT_DATE + INTERVAL '30' DAY""")
    incoming = cursor.fetchall()

    return render_template('concerts.html', incoming=incoming)
