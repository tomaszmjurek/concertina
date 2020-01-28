from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import PlaceForm, QueryForm
import psycopg2

from concertina.utils import *

places_bp = Blueprint('places', __name__)


@places_bp.route('/places')
@places_bp.route('/places/<string:query>')
def places(query=None):
    cursor.execute("SELECT * FROM PLACES ORDER BY CITY ASC, NAME ASC")
    places = cursor.fetchall()

    if query:
        places = filter_by_query(places, query)

    query_form = QueryForm()
    form = PlaceForm()

    form.to_edit.choices = Options.EMPTY + sorted([(x['id_place'], f'{x["name"]}/{x["city"]}') for x in places], key=lambda x: x[1])

    return render_template('places.html', places=places, form=form, query_form=query_form)


@places_bp.route('/places_search', methods=['POST'])
def places_search():
    form = QueryForm()
    query = form.query.data
    if not is_set(query):
        query = None
    return redirect(url_for('places.places', query=query))


@places_bp.route('/places', methods=['POST'])
def places_create():
    form = PlaceForm()
    name = form.name.data
    city = form.city.data
    to_edit = form.to_edit.data
    if not is_set(name) or not is_set(city) and not is_set(to_edit):
        flash('Name and city cannot be empty!')
        return redirect(url_for('places.places'))
    street = form.street.data

    if not is_set(to_edit):
        try:
            cursor.execute("INSERT INTO places(name, city, street)"
                           "VALUES(%s::TEXT, %s::TEXT, %s::TEXT)", (name, city, street))
        except psycopg2.IntegrityError as e:
            flash('Such a place already exists!')
        except Exception as e:
            flash('Some required fields were not set!')
    else:
        try:
            if is_set(name):
                cursor.execute("UPDATE PLACES SET name = %s::TEXT WHERE ID_PLACE = %s::INTEGER", (name, to_edit))
            if is_set(city):
                cursor.execute("UPDATE PLACES SET city = %s::TEXT WHERE ID_PLACE = %s::INTEGER", (city, to_edit))
            if is_set(street):
                cursor.execute("UPDATE PLACES SET street = %s::TEXT WHERE ID_PLACE = %s::INTEGER", (street, to_edit))
        except psycopg2.IntegrityError as e:
            flash('Such a place already exists!')
        except Exception as e:
            flash('Modification was not possible!')

    return redirect(url_for('places.places'))


@places_bp.route('/places/delete/<int:id_place>')
def places_delete(id_place):
    try:
        cursor.execute('DELETE FROM places WHERE id_place = %s::INTEGER', (id_place, ))
        flash('Place deleted sucessfully!')
    except:
        flash('Some events happen at this place!')
    return redirect(url_for('places.places'))