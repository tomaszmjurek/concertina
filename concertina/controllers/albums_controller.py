from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import AlbumForm
import psycopg2


albums_bp = Blueprint('albums', __name__)


@albums_bp.route('/')
@albums_bp.route('/homepage')
def homepage():
    return redirect(url_for('concerts.concerts'))


@albums_bp.route('/albums')
def albums():
    cursor.execute("SELECT name, band, genre FROM albums ORDER BY name")
    my_albums = cursor.fetchall()

    form = AlbumForm()

    cursor.execute("SELECT * FROM bands")
    bands = cursor.fetchall()
    form.band.choices = [(band['name'], band['name']) for band in bands]

    cursor.execute("SELECT * FROM genres")
    genres = cursor.fetchall()
    form.genre.choices = [(genre['name'], genre['name']) for genre in genres]

    return render_template('albums.html', my_albums=my_albums, form=form)


@albums_bp.route('/albums', methods=['POST'])
def albums_add():
    form = AlbumForm()
   # id_album = int(form.name.data) # TODO jak dodawac
    name = form.name.data
    band = form.band.data
    genre = form.genre.data

    try:
        cursor.execute("INSERT INTO albums(band, name, genre)"
                        "VALUES(%s::TEXT, %s::TEXT, %s::TEXT)",
                        (name, band, genre))
    except psycopg2.IntegrityError as e:
        start_pos = str(e).find('DETAIL') + 9
        flash(str(e)[start_pos:])

    return redirect(url_for('albums.albums'))


@albums_bp.route('/albums/delete/<int:id_album>')
def album_delete(id_album):
    cursor.execute("DELETE FROM albums WHERE id_album = %s::INTEGER", [id_album])
    flash("Album deleted successfully!")
    return redirect(url_for('albums.albums'))
