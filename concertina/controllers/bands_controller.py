from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import BandForm, QueryForm
import psycopg2

from concertina.utils import *

bands_bp = Blueprint('bands', __name__)


@bands_bp.route('/')
@bands_bp.route('/homepage')
def homepage():
    return redirect(url_for('concerts.concerts'))


@bands_bp.route('/bands')
@bands_bp.route('/bands/<string:query>')
def bands(query=None):
    cursor.execute("SELECT * FROM bands ORDER BY name")
    my_bands = cursor.fetchall()

    if query:
        my_bands = filter_by_query(my_bands, query)

    query_form = QueryForm()
    form = BandForm()

    form.to_edit.choices = Options.EMPTY + [(x['name'], x['name']) for x in my_bands]

    return render_template('bands.html', my_bands=my_bands, form=form, query_form=query_form)


@bands_bp.route('/bands_search', methods=['POST'])
def bands_search():
    form = QueryForm()
    query = form.query.data
    if not is_set(query):
        query = None
    return redirect(url_for('bands.bands', query=query))


@bands_bp.route('/bands', methods=['POST'])
def bands_add():
    form = BandForm()
    name = form.name.data
    formation_date = form.formation_date.data
    to_edit = form.to_edit.data

    if not is_set(to_edit):
        try:
            cursor.execute("INSERT INTO bands(name, formation_date)"
                           "VALUES(%s::TEXT, %s::DATE)",
                           (name, formation_date))
        except psycopg2.IntegrityError as e:
           flash('Such a band already exists!')
        except Exception as e:
            flash(Options.fields_not_set)
    else:
        try:
            if is_set(name):
                cursor.execute('UPDATE BANDS SET name = %s::TEXT WHERE name= %s::TEXT', (name, to_edit))
            if is_set(formation_date):
                cursor.execute('UPDATE BANDS SET formation_date = %s::DATE WHERE name= %s::TEXT', (formation_date, to_edit))
        except psycopg2.IntegrityError as e:
            flash('Such a band already exists!')
        except Exception as e:
            flash('Modification was not possible!')

    return redirect(url_for('bands.bands'))


@bands_bp.route('/bands/delete/<string:name>')
def band_delete(name):
    try:
        cursor.execute("DELETE FROM bands WHERE name = %s::TEXT", [name])
        flash("Band deleted successfully!")
    except:
        flash("Can't delete this band because it's not empty!")
    return redirect(url_for('bands.bands'))
