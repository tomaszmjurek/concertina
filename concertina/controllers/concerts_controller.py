from flask import render_template, Blueprint, redirect, url_for, flash

from concertina.app import cursor
from concertina.controllers.forms import ConcertForm, QueryForm
import psycopg2

from concertina.utils import *

concerts_bp = Blueprint('concerts', __name__)


@concerts_bp.route('/')
@concerts_bp.route('/homepage')
def homepage():
    return redirect(url_for('concerts.concerts'))


@concerts_bp.route('/concerts')
@concerts_bp.route('/concerts/<string:query>')
def concerts(query=None):
    cursor.execute("SELECT * FROM getConcertsByDate() NATURAL JOIN PLACES ORDER BY concert_date DESC")
    incoming = cursor.fetchall()
    if query:
        incoming = filter_by_query(incoming, query)

    form = ConcertForm()
    query_form = QueryForm()

    cursor.execute("SELECT * FROM bands")
    bands = cursor.fetchall()
    form.band.choices = Options.BLANK + sorted([(band['name'], band['name']) for band in bands], key=lambda x: x[1])

    cursor.execute("SELECT * FROM places")
    places = cursor.fetchall()
    form.place.choices = Options.BLANK + sorted([(place['id_place'], f'{place["city"]} / {place["name"]}')
                          for place in places], key=lambda x: x[1])

    form.to_edit.choices = Options.EMPTY + sorted([(x['id_concert'], x['id_concert']) for x in incoming], key=lambda x: x[1])

    return render_template('concerts.html', incoming=incoming, form=form, query_form=query_form)


@concerts_bp.route('/concerts_search', methods=['POST'])
def concerts_search():
    form = QueryForm()
    query = form.query.data
    if not is_set(query):
        query = None
    return redirect(url_for('concerts.concerts', query=query))



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
            cursor.execute("INSERT INTO concerts(band, concert_date, id_place)"
                            "VALUES(%s::TEXT, %s::DATE, %s::INTEGER)",
                            (band, concert_date, int(id_place)))
            if is_set(tour):
                cursor.execute('UPDATE CONCERTS SET tour = %s::TEXT'
                               ' WHERE band = %s::TEXT AND concert_date = %s::DATE AND id_place = %s::INTEGER',
                               (tour, band, concert_date, int(id_place)))
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
