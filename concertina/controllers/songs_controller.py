from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import SongForm
import psycopg2

from concertina.utils import *

songs_bp = Blueprint('songs', __name__)


@songs_bp.route('/songs/<int:id_album>')
def songs(id_album):
    cursor.execute("SELECT * FROM songs WHERE id_album = %s::INTEGER order by position", [id_album])
    my_songs = cursor.fetchall()

    cursor.execute("SELECT name, band FROM albums WHERE id_album = %s::INTEGER", [id_album])
    album_info = cursor.fetchone()

    form = SongForm()

    form.to_edit.choices = Options.EMPTY + sorted([(x['name'], x['position']) for x in my_songs], key=lambda x: x[1])

    return render_template('songs.html', my_songs=my_songs, id_album=id_album,
                           album_name=album_info['name'], band=album_info['band'], form=form)


@songs_bp.route('/songs/<int:id_album>', methods=['POST'])
def songs_add(id_album):
    form = SongForm()
    name = form.name.data
    to_edit = form.to_edit.data

    if not is_set(name) and not is_set(to_edit):
        flash('Name cannot be empty!')
        return redirect(url_for('songs.songs'))
    position = form.position.data
    length = form.length.data

    if not is_set(to_edit):
        try:
            cursor.execute("INSERT INTO songs(name, id_album, position)"
                           "VALUES(%s::TEXT, %s::INTEGER, %s::INTEGER)",
                            (name, id_album, position))
            if is_set(length):
                cursor.execute('UPDATE SONGS SET length = %s::INTEGER WHERE name= %s::TEXT', (length, name))
        except psycopg2.IntegrityError as e:
            flash('Such a song already exists!')
        except Exception as e:
            flash(Options.fields_not_set)
    else:
        try:
            if is_set(name):
                cursor.execute('UPDATE SONGS SET name = %s::TEXT WHERE name= %s::TEXT', (name, to_edit))
            if is_set(position):
                cursor.execute('UPDATE SONGS SET position = %s::INTEGER WHERE name= %s::TEXT', (position, to_edit))
            if is_set(length):
                cursor.execute('UPDATE SONGS SET length = %s::INTEGER WHERE name= %s::TEXT', (length, to_edit))

        except psycopg2.IntegrityError as e:
            flash('Such a song already exists!')
        except Exception as e:
            flash('Modification was not possible!')

    return redirect(url_for('songs.songs', id_album=id_album))


@songs_bp.route('/songs/delete/<int:id_song>/<int:id_album>')
def song_delete(id_song, id_album):

    cursor.execute("DELETE FROM songs WHERE id_song = %s::INTEGER", [id_song])
    flash("Song deleted successfully!")
    return redirect(url_for('songs.songs', id_album=id_album))
