from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import SongForm
import psycopg2


songs_bp = Blueprint('songs', __name__)


@songs_bp.route('/songs/<int:id_album>')
def songs(id_album):
    cursor.execute("SELECT * FROM songs WHERE id_album = %s::INTEGER  order by position", [id_album])
    my_songs = cursor.fetchall()

    form = SongForm()

    return render_template('songs.html', my_songs=my_songs, form=form)


@songs_bp.route('/songs/<int:id_album>', methods=['POST'])
def songs_add(id_album):
    form = SongForm()
    # album_name = form.album_name.data
    position = form.position.data
    name = form.name.data

    # cursor.execute("SELECT id_album FROM albums WHERE name = %s::TEXT", [album_name])
    # id_album = cursor.fetchall()

    try:
        cursor.execute("INSERT INTO songs(position, name, id_album)"
                       "VALUES(%s::INTEGER, %s::TEXT, %s::INTEGER)",
                        (position, name, id_album))
    except psycopg2.IntegrityError as e:
        start_pos = str(e).find('DETAIL') + 9
        flash(str(e)[start_pos:])

    return redirect(url_for('songs.songs', id_album=id_album))


@songs_bp.route('/songs/delete/<int:id_song>')
def song_delete(id_song):
    cursor.execute("SELECT id_album FROM songs WHERE id_song = %s::INTEGER", [id_song])
    id_album = cursor.fetchall()

    cursor.execute("DELETE FROM songs WHERE id_song = %s::INTEGER", [id_song])
    flash("Song deleted successfully!")
    return redirect(url_for('songs.songs', id_album=id_album))
