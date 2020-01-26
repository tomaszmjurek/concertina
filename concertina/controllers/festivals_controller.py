from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import FestivalForm
import psycopg2

festivals_bp = Blueprint('festivals', __name__)


@festivals_bp.route('/festivals')
def festivals():
    cursor.execute("SELECT * FROM festivals NATURAL JOIN places ORDER BY date_start DESC")
    incoming = cursor.fetchall()

    form = FestivalForm()

    cursor.execute("SELECT * FROM places")
    places = cursor.fetchall()
    form.place.choices = [(place['id_place'], f'{place["city"]} / {place["name"]}')
                          for place in places]

    return render_template('festivals.html', incoming=incoming, form=form)


@festivals_bp.route('/festivals', methods=['POST'])
def festivals_add():
    form = FestivalForm()
    name = form.data.name
    id_place = int(form.place.data)
    date_start = form.date_start.data

    try:
        cursor.execute("INSERT INTO festivals(name, date_start, id_place)"
                       "VALUES (%s::TEXT, %s::DATE, %s::INTEGER)",
                       (name, date_start, id_place))
    except psycopg2.IntegrityError as e:
        start_pos = str(e).find('DETAIL') + 9
        flash(str(e)[start_pos:])

    return redirect(url_for('festivals.festivals'))


@festivals_bp.route('/festivals/delete/<int:id_festival>')
def festivals_delete(id_festival):
    cursor.execute('DELETE FROM festivals WHERE id_festival = %s::INTEGER', [id_festival])
    flash('Festival delete successfully')
    return redirect(url_for('festivals.festivals'))