from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import BandForm
import psycopg2

bands_bp = Blueprint('bands', __name__)


@bands_bp.route('/')
@bands_bp.route('/homepage')
def homepage():
    return redirect(url_for('concerts.concerts'))


@bands_bp.route('/bands')
def bands():
    cursor.execute("SELECT * FROM bands ORDER BY name")
    mybands = cursor.fetchall()

    form = BandForm()

    return render_template('bands.html', mybands=mybands, form=form)  # incoming=incoming,


@bands_bp.route('/bands', methods=['POST'])
def bands_add():
    form = BandForm()
    name = form.name.data
    formation_date = form.formation_date.data

    try:
        cursor.execute("INSERT INTO bands(name, formation_date)"
                       "VALUES(%s::TEXT, %s::DATE)",
                       (name, formation_date))
    except psycopg2.IntegrityError as e:
        start_pos = str(e).find('DETAIL') + 9
        flash(str(e)[start_pos:])

    return redirect(url_for('bands.bands'))


@bands_bp.route('/bands/delete/<string:name>')
def band_delete(name):
    cursor.execute("DELETE FROM bands WHERE name = %s::TEXT", [name])
    flash("Band deleted successfully!")
    return redirect(url_for('bands.bands'))
