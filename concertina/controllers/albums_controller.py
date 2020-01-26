from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import AlbumForm
import psycopg2

from concertina.utils import *

albums_bp = Blueprint('albums', __name__)


@albums_bp.route('/')
@albums_bp.route('/homepage')
def homepage():
    return redirect(url_for('concerts.concerts'))


@albums_bp.route('/albums')
def albums():
    cursor.execute("SELECT * FROM albums ORDER BY name")
    my_albums = cursor.fetchall()

    form = AlbumForm()

    cursor.execute("SELECT * FROM bands")
    bands = cursor.fetchall()
    form.band.choices = Options.BLANK + [(band['name'], band['name']) for band in bands]

    cursor.execute("SELECT * FROM genres")
    genres = cursor.fetchall()
    form.genre.choices = Options.BLANK + [(genre['name'], genre['name']) for genre in genres]

    form.to_edit.choices = Options.EMPTY + [(x['name'], x['name']) for x in my_albums]

    return render_template('albums.html', my_albums=my_albums, form=form)


@albums_bp.route('/albums', methods=['POST'])
def albums_add():
    form = AlbumForm()
    name = form.name.data
    band = form.band.data
    genre = form.genre.data
    to_edit = form.to_edit.data

    if not is_set(to_edit):
        try:
            cursor.execute("INSERT INTO albums(band, name, genre)"
                           "VALUES(%s::TEXT, %s::TEXT, %s::TEXT)",
                           (name, band, genre))
        except psycopg2.IntegrityError as e:
            flash('Such album already exists!')
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
