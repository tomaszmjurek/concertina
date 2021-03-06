from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import AlbumForm, QueryForm
import psycopg2

from concertina.utils import *

albums_bp = Blueprint('albums', __name__)


@albums_bp.route('/')
@albums_bp.route('/homepage')
def homepage():
    return redirect(url_for('concerts.concerts'))


@albums_bp.route('/albums')
@albums_bp.route('/albums/<string:query>')
def albums(query=None):
    cursor.execute("SELECT * FROM albums ORDER BY band, name")
    my_albums = cursor.fetchall()
    if query:
        my_albums = filter_by_query(my_albums, query)

    form = AlbumForm()
    query_form = QueryForm()

    cursor.execute("SELECT * FROM bands")
    bands = cursor.fetchall()
    form.band.choices = Options.BLANK + sorted([(band['name'], band['name']) for band in bands], key=lambda x: x[1])

    cursor.execute("SELECT * FROM genres")
    genres = cursor.fetchall()
    form.genre.choices = Options.BLANK + sorted([(genre['name'], genre['name']) for genre in genres], key=lambda x: x[1])

    form.to_edit.choices = Options.EMPTY + sorted([(x['name'], x['name']) for x in my_albums], key=lambda x: x[1])

    return render_template('albums.html', my_albums=my_albums, form=form, query_form=query_form)

@albums_bp.route('/albums_search', methods=['POST'])
def albums_search():
    form = QueryForm()
    query = form.query.data
    if not is_set(query):
        query = None
    return redirect(url_for('albums.albums', query=query))


@albums_bp.route('/albums', methods=['POST'])
def albums_add():
    form = AlbumForm()
    name = form.name.data
    to_edit = form.to_edit.data
    if not is_set(name) and not is_set(to_edit):
        flash('Name cannot be empty!')
        return redirect(url_for('albums.albums'))
    band = form.band.data
    genre = form.genre.data

    if not is_set(to_edit):
        try:
            cursor.execute("INSERT INTO albums(band, name)"
                           "VALUES(%s::TEXT, %s::TEXT)",
                           (band, name))
            if is_set(genre):
                cursor.execute('UPDATE albums SET genre = %s::TEXT WHERE band = %s::TEXT'
                               'AND name = %s::TEXT', (genre, band, name))
        except psycopg2.IntegrityError as e:
            flash('Such an album already exists!')
        except Exception as e:
            flash(Options.fields_not_set)
    else:
        try:
            if is_set(name):
                cursor.execute('UPDATE albums SET name = %s::TEXT WHERE name= %s::TEXT', (name, to_edit))
            if is_set(band):
                cursor.execute('UPDATE albums SET band = %s::TEXT WHERE name= %s::TEXT', (band, to_edit))
            if is_set(genre):
                cursor.execute('UPDATE albums SET genre = %s::TEXT WHERE name= %s::TEXT', (genre, to_edit))
        except psycopg2.IntegrityError as e:
            flash('Such album already exists!')
        except Exception as e:
            flash('Modification was not possible!')

    return redirect(url_for('albums.albums'))


@albums_bp.route('/albums/delete/<int:id_album>')
def album_delete(id_album):
    cursor.execute("DELETE FROM albums WHERE id_album = %s::INTEGER", [id_album])
    flash("Album deleted successfully!")
    return redirect(url_for('albums.albums'))
