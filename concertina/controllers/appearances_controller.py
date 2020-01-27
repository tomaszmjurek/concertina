from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import AppearanceForm, QueryForm
import psycopg2

from concertina.utils import *

appearances_bp = Blueprint('appearances', __name__)


@appearances_bp.route('/appearances/<int:id_festival>')
@appearances_bp.route('/appearances/<int:id_festival>/<string:query>')
def appearances(id_festival=None, query=None):

    cursor.execute("SELECT * FROM bands b JOIN appearances a ON b.name = a.band "
                   "WHERE a.id_festival = %s::INTEGER order by b.name", [id_festival])
    my_bands = cursor.fetchall()

    if query:
        my_bands = filter_by_query(my_bands, query)

    form = AppearanceForm()
    query_form = QueryForm()

    cursor.execute("SELECT * FROM bands")
    bands = cursor.fetchall()
    form.band.choices = Options.BLANK + sorted([(band['name'], band['name']) for band in bands], key=lambda x: x[1])

    return render_template('appearances.html', my_bands=my_bands, query_form=query_form, form=form, id_festival=id_festival)


@appearances_bp.route('/appearances_search', methods=['POST'])
def appearances_search():
    form = QueryForm()
    query = form.query.data
    if not is_set(query):
        query = None
    return redirect(url_for('appearances.appearances', query=query))


@appearances_bp.route('/appearances/<int:id_festival>', methods=['POST'])
def appearances_add(id_festival):
    form = AppearanceForm()
    band = form.band.data

    try:
        cursor.execute("INSERT INTO appearances (id_festival, band)"
                       "VALUES(%s::INTEGER, %s::TEXT)", (id_festival, band))
    except psycopg2.IntegrityError as e:
        flash('That band is already participating!')
    except Exception as e:
        flash(Options.fields_not_set)

    return redirect(url_for('appearances.appearances', id_festival=id_festival))


@appearances_bp.route('/appearances/delete/<string:band>/<int:id_festival>')
def appearance_delete(band, id_festival):

    cursor.execute("DELETE FROM appearances WHERE band = %s::TEXT AND "
                   "id_festival = %s::INTEGER", (band, id_festival))
    flash("Band successfully deleted from festival!")
    return redirect(url_for('appearances.appearances', id_festival=id_festival))
