from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import SongForm
import psycopg2


songs_bp = Blueprint('songs', __name__)


@songs_bp.route('/songs/<int:id_album>')
def songs(id_album):
    cursor.execute("SELECT * FROM songs WHERE id_album = %s::INTEGER order by position", [id_album])
    my_songs = cursor.fetchall()

    cursor.execute("SELECT name, band FROM albums WHERE id_album = %s::INTEGER", [id_album])
    album_info = cursor.fetchone()

    form = SongForm()

    return render_template('songs.html', my_songs=my_songs, id_album=id_album,
                           album_name=album_info['name'], band=album_info['band'], form=form)


@songs_bp.route('/songs/<int:id_album>', methods=['POST'])
def songs_add(id_album):
    form = SongForm()
    name = form.name.data

    try:
        cursor.execute("INSERT INTO songs(name, id_album)"
                       "VALUES(%s::TEXT, %s::INTEGER)",
                        (name, id_album))
    except psycopg2.IntegrityError as e:
        start_pos = str(e).find('DETAIL') + 9
        flash(str(e)[start_pos:])

    return redirect(url_for('songs.songs', id_album=id_album))


@songs_bp.route('/songs/delete/<int:id_song>/<int:id_album>')
def song_delete(id_song, id_album):

    cursor.execute("DELETE FROM songs WHERE id_song = %s::INTEGER", [id_song])
    flash("Song deleted successfully!")
    return redirect(url_for('songs.songs', id_album=id_album))
