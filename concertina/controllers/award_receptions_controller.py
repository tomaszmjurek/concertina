from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import AwardReceptionForm, QueryForm
import psycopg2

from concertina.utils import *

award_receptions_bp = Blueprint('award_receptions', __name__)


@award_receptions_bp.route('/award_receptions/<string:award>')
@award_receptions_bp.route('/award_receptions/<string:award>/<string:query>')
def award_receptions(award=None, query=None):

    cursor.execute("SELECT * FROM albums al JOIN award_receptions a ON a.id_album = al.id_album "
                   "WHERE a.award = %s::TEXT order by a.award", [award])
    awards_albums = cursor.fetchall()

    if query:
        awards_albums = filter_by_query(awards_albums, query)

    form = AwardReceptionForm()
    query_form = QueryForm()

    cursor.execute("SELECT * FROM albums")
    albums = cursor.fetchall()
    form.album.choices = Options.BLANK + sorted([(album['name'], album['name']) for album in albums], key=lambda x: x[1])

    return render_template('award_receptions.html', my_award_receptions=awards_albums, query_form=query_form, form=form, award_name=award)


@award_receptions_bp.route('/albums_search', methods=['POST'])
def albums_search():
    form = QueryForm()
    query = form.query.data
    if not is_set(query):
        query = None
    return redirect(url_for('albums.albums', query=query))


@award_receptions_bp.route('/award_receptions/<string:award>', methods=['POST'])
def award_receptions_add(award):
    form = AwardReceptionForm()
    album = form.album.data

    cursor.execute("SELECT id_album FROM albums WHERE name = %s::TEXT", (album,))
    id_album = cursor.fetchone()

    try:
        cursor.execute("INSERT INTO award_receptions(id_album, award)"
                       "VALUES(%s::INTEGER, %s::TEXT)", (id_album["id_album"], award))
    except psycopg2.IntegrityError as e:
        flash('That album already has the award!')
    except Exception as e:
        flash(Options.fields_not_set)

    return redirect(url_for('award_receptions.award_receptions', award=award))


@award_receptions_bp.route('/award_receptions/delete/<string:award>/<int:id_album>')
def award_reception_delete(award, id_album):

    cursor.execute("DELETE FROM award_receptions WHERE award = %s::TEXT AND "
                   "id_album = %s::INTEGER", (award, id_album))
    flash("award_reception deleted successfully!")
    return redirect(url_for('award_receptions.award_receptions', award=award))
