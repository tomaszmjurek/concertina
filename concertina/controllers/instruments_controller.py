from flask import render_template, Blueprint, redirect, url_for, flash
from concertina.app import cursor
from concertina.controllers.forms import InstrumentForm
import psycopg2

instruments_bp = Blueprint('instruments', __name__)


@instruments_bp.route('/instruments')
def instruments():
    cursor.execute("SELECT * FROM INSTRUMENTS ORDER BY TYPE ASC")
    instruments = cursor.fetchall()

    form = InstrumentForm()

    return render_template('instruments.html', instruments=instruments, form=form)


@instruments_bp.route('/instruments', methods=['POST'])
def instruments_create():
    form = InstrumentForm()
    type = form.type.data
    try:
        cursor.execute("INSERT INTO instruments(type) VALUES(%s::TEXT)", (type, ))
    except psycopg2.IntegrityError as e:
        flash('Such an instrument already exists!')
    except Exception as e:
        flash('Some required fields were not set!')

    return redirect(url_for('instruments.instruments'))


@instruments_bp.route('/instruments/delete/<string:type>')
def instruments_delete(type):
    cursor.execute('DELETE FROM instruments WHERE type = %s::TEXT', (type, ))
    flash('Instrument deleted sucessfully!')
    return redirect(url_for('instruments.instruments'))