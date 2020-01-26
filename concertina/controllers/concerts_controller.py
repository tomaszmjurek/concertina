from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import ConcertForm
import psycopg2


concerts_bp = Blueprint('concerts', __name__)


@concerts_bp.route('/')
@concerts_bp.route('/homepage')
def homepage():
    return redirect(url_for('concerts.concerts'))


@concerts_bp.route('/concerts')
def concerts():
    cursor.execute("SELECT * FROM getConcertsByDate() NATURAL JOIN PLACES")
    incoming = cursor.fetchall()

    form = ConcertForm()

    cursor.execute("SELECT * FROM bands")
    bands = cursor.fetchall()
    form.band.choices = [(band['name'], band['name']) for band in bands]

    cursor.execute("SELECT * FROM places")
    places = cursor.fetchall()
    form.place.choices = [(place['id_place'], f'{place["city"]} / {place["name"]}')
                          for place in places]

    return render_template('concerts.html', incoming=incoming, form=form)


@concerts_bp.route('/concerts', methods=['POST'])
def concerts_add():
    form = ConcertForm()
    band = form.band.data
    id_place = int(form.place.data)
    concert_date = form.concert_date.data
    tour = form.tour.data

    try:
        cursor.execute("INSERT INTO concerts(band, concert_date, tour, id_place)"
                        "VALUES(%s::TEXT, %s::DATE, %s::TEXT, %s::INTEGER)",
                        (band, concert_date, tour, id_place))
    except psycopg2.IntegrityError as e:
        start_pos = str(e).find('DETAIL') + 9
        flash(str(e)[start_pos:])

    return redirect(url_for('concerts.concerts'))


@concerts_bp.route('/concerts/delete/<int:id_concert>')
def concert_delete(id_concert):
    cursor.execute("DELETE FROM CONCERTS WHERE id_concert = %s::INTEGER", [id_concert])
    flash("Concert deleted successfully!")
    return redirect(url_for('concerts.concerts'))


@concerts_bp.route('/concerts/modify/<int:id_concert>')
def concert_modify(id_concert):
    return redirect(url_for('concerts,concerts'))
