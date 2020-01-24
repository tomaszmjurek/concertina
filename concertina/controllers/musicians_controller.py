from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import MusicianForm
import psycopg2


musicians_bp = Blueprint('musicians', __name__)


@musicians_bp.route('/')
@musicians_bp.route('/homepage')
def homepage():
    return redirect(url_for('concerts.concerts'))


@musicians_bp.route('/musicians')
def musicians():
    cursor.execute("SELECT * FROM musicians order by name")
    my_musicians = cursor.fetchall()

    form = MusicianForm()

    cursor.execute("SELECT * FROM bands")
    bands = cursor.fetchall()
    form.band.choices = [(band['name'], band['name']) for band in bands]

    cursor.execute("SELECT * FROM instruments")
    instruments = cursor.fetchall()
    form.instrument.choices = [(instrument['type'], instrument['type'])
                               for instrument in instruments]

    return render_template('musicians.html', my_musicians=my_musicians, form=form)


@musicians_bp.route('/musicians', methods=['POST'])
def musicians_add():
    form = MusicianForm()
    name = form.name.data
    band = form.band.data
    instrument = form.instrument.data

    try:
        cursor.execute("INSERT INTO musicians(name, band, instrument)"
                        "VALUES(%s::TEXT, %s::TEXT, %s::TEXT)",
                        (name, band, instrument))
    except psycopg2.IntegrityError as e:
        start_pos = str(e).find('DETAIL') + 9
        flash(str(e)[start_pos:])

    return redirect(url_for('musicians.musicians'))


@musicians_bp.route('/musicians/delete/<string:name>')
def musician_delete(name):
    cursor.execute("DELETE FROM musicians WHERE name = %s::TEXT", [name])
    flash("Musician deleted successfully!")
    return redirect(url_for('musicians.musicians'))
