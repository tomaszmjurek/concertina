from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import FestivalForm
import psycopg2

from concertina.utils import *

festivals_bp = Blueprint('festivals', __name__)
BLANK_OPTION = [(None, 'Fill this')]


@festivals_bp.route('/festivals')
def festivals():
    cursor.execute("SELECT * FROM festivals f JOIN PLACES p  ON  f.id_place = p.id_place ORDER BY f.date_start DESC")
    incoming = cursor.fetchall()

    form = FestivalForm()

    cursor.execute("SELECT * FROM places")
    places = cursor.fetchall()
    form.place.choices = BLANK_OPTION + [(place['id_place'], f'{place["city"]} / {place["name"]}')
                                         for place in places]

    form.to_edit.choices = Options.EMPTY + [(x['id_festival'], x['id_festival']) for x in incoming]

    return render_template('festivals.html', incoming=incoming, form=form)


@festivals_bp.route('/festivals', methods=['POST'])
def festivals_add():
    form = FestivalForm()
    name = form.name.data
    id_place = form.place.data
    date_start = form.date_start.data
    to_edit = form.to_edit.data

    if not is_set(to_edit):
        try:
            cursor.execute("INSERT INTO festivals(name, date_start, id_place)"
                           "VALUES (%s::TEXT, %s::DATE, %s::INTEGER)",
                           (name, date_start, int(id_place)))
        except psycopg2.IntegrityError as e:
            start_pos = str(e).find('DETAIL') + 9
            flash(str(e)[start_pos:])
    else:
        try:
            if is_set(name):
                cursor.execute('UPDATE FESTIVALS SET name = %s::TEXT WHERE ID_FESTIVAL = %s::INTEGER', (name, to_edit))
            if is_set(id_place):
                cursor.execute('UPDATE FESTIVALS SET id_place = %s::INTEGER WHERE ID_FESTIVAL = %s::INTEGER',
                               (int(id_place), to_edit))
            if is_set(date_start):
                cursor.execute('UPDATE FESTIVALS SET date_start = %s::DATE WHERE ID_FESTIVAL = %s::INTEGER',
                               (date_start, to_edit))

        except psycopg2.IntegrityError as e:
            start_pos = str(e).find('DETAIL') + 9
            flash(str(e)[start_pos:])
        except Exception as e:
            flash('Modification was not possible!')

    return redirect(url_for('festivals.festivals'))


@festivals_bp.route('/festivals/delete/<int:id_festival>')
def festivals_delete(id_festival):
    cursor.execute('DELETE FROM festivals WHERE id_festival = %s::INTEGER', [id_festival])
    flash('Festival delete successfully')
    return redirect(url_for('festivals.festivals'))
