from flask import render_template, Blueprint, redirect, url_for, flash

from concertina.app import cursor
from concertina.controllers.forms import ConcertForm
import psycopg2

from concertina.utils import *

concerts_bp = Blueprint('concerts', __name__)


@concerts_bp.route('/')
@concerts_bp.route('/homepage')
def homepage():
    return redirect(url_for('concerts.concerts'))


@concerts_bp.route('/concerts')
def concerts():
    cursor.execute("SELECT * FROM getConcertsByDate() NATURAL JOIN PLACES ORDER BY concert_date DESC")
    incoming = cursor.fetchall()

    form = ConcertForm()

    cursor.execute("SELECT * FROM bands")
    bands = cursor.fetchall()
    form.band.choices = Options.BLANK + [(band['name'], band['name']) for band in bands]

    cursor.execute("SELECT * FROM places")
    places = cursor.fetchall()
    form.place.choices = Options.BLANK + [(place['id_place'], f'{place["city"]} / {place["name"]}')
                          for place in places]

    form.to_edit.choices = Options.EMPTY + [(x['id_concert'], x['id_concert']) for x in incoming]

    return render_template('concerts.html', incoming=incoming, form=form)


@concerts_bp.route('/concerts', methods=['POST'])
def concerts_add():
    form = ConcertForm()
    band = form.band.data
    id_place = form.place.data
    concert_date = form.concert_date.data
    tour = form.tour.data
    to_edit = form.to_edit.data

    if not is_set(to_edit):
        try:
            cursor.execute("INSERT INTO concerts(band, concert_date, tour, id_place)"
                            "VALUES(%s::TEXT, %s::DATE, %s::TEXT, %s::INTEGER)",
                            (band, concert_date, tour, int(id_place)))
        except psycopg2.IntegrityError as e:
            flash('Such a concert already exists!')
        except Exception as e:
            flash('Some required fields were not set!')
    else:
        try:
            if is_set(band):
                cursor.execute('UPDATE CONCERTS SET band = %s::TEXT WHERE id_concert = %s::INTEGER', (band, to_edit))
            if is_set(id_place):
                cursor.execute('UPDATE CONCERTS SET id_place = %s::INTEGER WHERE id_concert = %s::INTEGER',
                               (int(id_place), to_edit))
            if is_set(concert_date):
                cursor.execute('UPDATE CONCERTS SET concert_date = %s::DATE WHERE id_concert = %s::INTEGER',
                               (concert_date, to_edit))
            if is_set(tour):
                cursor.execute('UPDATE CONCERTS SET tour = %s::TEXT WHERE id_concert = %s::INTEGER', (tour, to_edit))

        except psycopg2.IntegrityError as e:
            flash('Such a concert already exists!')
        except Exception as e:
            flash('Modification was not possible!')

    return redirect(url_for('concerts.concerts'))


@concerts_bp.route('/concerts/delete/<int:id_concert>')
def concert_delete(id_concert):
    cursor.execute("DELETE FROM CONCERTS WHERE id_concert = %s::INTEGER", [id_concert])
    flash("Concert deleted successfully!")
    return redirect(url_for('concerts.concerts'))
