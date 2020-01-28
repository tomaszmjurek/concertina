from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import GenreForm, QueryForm
import psycopg2

from concertina.utils import *

genres_bp = Blueprint('genres', __name__)


@genres_bp.route('/genres')
@genres_bp.route('/genres/<string:query>')
def genres(query=None):
    cursor.execute("SELECT * FROM genres ORDER BY name ASC")
    genres = cursor.fetchall()

    if query:
        genres = filter_by_query(genres, query)

    query_form = QueryForm()
    form = GenreForm()

    form.supergenre.choices = Options.BLANK + sorted([(x['name'], x['name']) for x in genres], key=lambda x: x[1])
    form.to_edit.choices = Options.EMPTY + sorted([(x['name'], x['name']) for x in genres], key=lambda x: x[1])

    return render_template('genres.html', genres=genres, form=form, query_form=query_form)


@genres_bp.route('/genres_search', methods=['POST'])
def genres_search():
    form = QueryForm()
    query = form.query.data
    if not is_set(query):
        query = None
    return redirect(url_for('genres.genres', query=query))


@genres_bp.route('/genres', methods=['POST'])
def genres_create():
    form = GenreForm()
    name = form.name.data
    to_edit = form.to_edit.data
    if not is_set(name) and not is_set(to_edit):
        flash('Name cannot be empty!')
        return redirect(url_for('genres.genres'))
    supergenre = form.supergenre.data

    if not is_set(to_edit):
        try:
            cursor.execute("INSERT INTO genres(name)"
                           "VALUES(%s::TEXT)", (name,))
            if is_set(supergenre):
                cursor.execute('UPDATE genres SET supergenre = %s::TEXT WHERE name= %s::TEXT',
                               (supergenre, name))
        except psycopg2.IntegrityError as e:
            flash('Such a genre already exists!')
        except Exception as e:
            flash('Some required fields were not set!')
    else:
        try:
            if is_set(name):
                cursor.execute('UPDATE genres SET name = %s::TEXT WHERE name = %s::TEXT', (name, to_edit))
            if is_set(supergenre):
                cursor.execute('UPDATE genres SET supergenre = %s::TEXT WHERE name = %s::TEXT', (supergenre, to_edit))
        except psycopg2.IntegrityError as e:
            flash('Such a genre already exists!')
        except Exception as e:
            flash('Modification was not possible!')

    return redirect(url_for('genres.genres'))


@genres_bp.route('/genres/delete/<string:name>')
def genres_delete(name):
    try:
        cursor.execute('DELETE FROM genres WHERE name = %s::TEXT', (name, ))
        flash('Genre deleted sucessfully!')
    except:
        flash('Some albums are of this genre!')
    return redirect(url_for('genres.genres'))
