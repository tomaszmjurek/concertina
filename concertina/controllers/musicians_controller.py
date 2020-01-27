from flask import render_template, Blueprint, redirect, url_for, flash, request
from concertina.app import cursor
from concertina.controllers.forms import MusicianForm, QueryForm
import psycopg2

from concertina.utils import *

musicians_bp = Blueprint('musicians', __name__)


@musicians_bp.route('/musicians')
@musicians_bp.route('/musicians/<string:query>')
def musicians(query=None):
    cursor.execute("SELECT * FROM musicians ORDER BY band, name")
    my_musicians = cursor.fetchall()
    if query:
        my_musicians = filter_by_query(my_musicians, query)

    form = MusicianForm()
    query_form = QueryForm()

    cursor.execute("SELECT * FROM bands")
    bands = cursor.fetchall()
    form.band.choices = Options.BLANK + sorted([(band['name'], band['name']) for band in bands], key=lambda x: x[1])

    cursor.execute("SELECT * FROM instruments")
    instruments = cursor.fetchall()
    form.instrument.choices = Options.BLANK + sorted([(instrument['type'], instrument['type'])
                               for instrument in instruments], key=lambda x: x[1])

    form.to_edit.choices = Options.EMPTY + [(x['name'], x['name']) for x in my_musicians]

    return render_template('musicians.html', my_musicians=my_musicians, form=form, query_form=query_form)


@musicians_bp.route('/musicians_search', methods=['POST'])
def musicians_search():
    form = QueryForm()
    query = form.query.data
    if not is_set(query):
        query = None
    return redirect(url_for('musicians.musicians', query=query))


@musicians_bp.route('/musicians', methods=['POST'])
def musicians_add():
    form = MusicianForm()
    name = form.name.data
    if not is_set(name):
        flash('Name cannot be empty!')
        return redirect(url_for('musicians.musicians'))
    band = form.band.data
    nationality = form.nationality.data
    instrument = form.instrument.data
    to_edit = form.to_edit.data

    if not is_set(to_edit):
        try:
            cursor.execute("INSERT INTO musicians(name, band, instrument)"
                            "VALUES(%s::TEXT, %s::TEXT, %s::TEXT)",
                            (name, band, instrument))
            if is_set(nationality):
                cursor.execute('UPDATE MUSICIANS SET nationality = %s::TEXT WHERE name= %s::TEXT', (nationality, name))
        except psycopg2.IntegrityError as e:
            flash('Such a musician already exists!')
        except Exception as e:
            flash(Options.fields_not_set)
    else:
        try:
            if is_set(name):
                cursor.execute('UPDATE MUSICIANS SET name = %s::TEXT WHERE name= %s::TEXT', (name, to_edit))
            if is_set(band):
                cursor.execute('UPDATE MUSICIANS SET band = %s::TEXT WHERE name= %s::TEXT', (band, to_edit))
            if is_set(instrument):
                cursor.execute('UPDATE MUSICIANS SET instrument = %s::TEXT WHERE name= %s::TEXT', (instrument, to_edit))
            if is_set(nationality):
                cursor.execute('UPDATE MUSICIANS SET nationality = %s::TEXT WHERE name= %s::TEXT', (nationality, to_edit))

        except psycopg2.IntegrityError as e:
            flash('Such a musician already exists!')
        except Exception as e:
            flash('Modification was not possible!')


    return redirect(url_for('musicians.musicians'))


@musicians_bp.route('/musicians/delete/<string:name>')
def musician_delete(name):
    cursor.execute("DELETE FROM musicians WHERE name = %s::TEXT", [name])
    flash("Musician deleted successfully!")
    return redirect(url_for('musicians.musicians'))
