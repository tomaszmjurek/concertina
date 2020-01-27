from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import AwardForm, QueryForm
import psycopg2

from concertina.utils import *

awards_bp = Blueprint('awards', __name__)


@awards_bp.route('/awards')
@awards_bp.route('/awards/<string:query>')
def awards(query=None):
    cursor.execute("SELECT * FROM awards ORDER BY name ASC")
    awards = cursor.fetchall()

    if query:
        awards = filter_by_query(awards, query)

    query_form = QueryForm()
    form = AwardForm()

    form.to_edit.choices = Options.EMPTY + sorted([(x['name'], x['name']) for x in awards], key=lambda x: x[1])

    return render_template('awards.html', awards=awards, form=form, query_form=query_form)


@awards_bp.route('/awards_search', methods=['POST'])
def awards_search():
    form = QueryForm()
    query = form.query.data
    if not is_set(query):
        query = None
    return redirect(url_for('awards.awards', query=query))


@awards_bp.route('/awards', methods=['POST'])
def awards_add():
    form = AwardForm()
    name = form.name.data
    if not is_set(name):
        flash('Name cannot be empty!')
        return redirect(url_for('awards.awards'))
    to_edit = form.to_edit.data

    if not is_set(to_edit):
        try:
            cursor.execute("INSERT INTO awards(name)"
                           "VALUES(%s::TEXT)",
                           (name,))
        except psycopg2.IntegrityError as e:
            flash('Such a award already exists!')
        except Exception as e:
            flash(Options.fields_not_set)
    else:
        try:
            if is_set(name):
                cursor.execute('UPDATE awardS SET name = %s::TEXT WHERE name= %s::TEXT', (name, to_edit))
        except psycopg2.IntegrityError as e:
            flash('Such a award already exists!')
        except Exception as e:
            flash('Modification was not possible!')

    return redirect(url_for('awards.awards'))


@awards_bp.route('/awards/delete/<string:name>')
def award_delete(name):
    try:
        cursor.execute("DELETE FROM awards WHERE name = %s::TEXT", [name])
        flash("Award deleted successfully!")
    except:
        flash("Can't delete this award!")
    return redirect(url_for('awards.awards'))
