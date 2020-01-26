from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from datetime import date


class ConcertForm(FlaskForm):
    band = SelectField('Band', choices=[], validators=[DataRequired()])
    place = SelectField('Place', choices=[], validators=[DataRequired()])
    concert_date = DateField('Concert date', validators=[DataRequired()])
    tour = StringField('Tour')
    to_edit = SelectField('To edit')
    submit = SubmitField('Add / Edit')


class BandForm(FlaskForm):
    name = StringField('Name')
    formation_date = DateField('Formation date', default=date.today())
    to_edit = SelectField('To edit')
    submit = SubmitField('Add / Edit')


class MusicianForm(FlaskForm):
    name = StringField('Name')
    band = SelectField('Band', choices=[], validators=[DataRequired()])
    instrument = SelectField('Instrument', choices=[], validators=[DataRequired()])
    to_edit = SelectField('To edit')
    submit = SubmitField('Add / Edit')


class FestivalForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date_start = DateField('Start date', validators=[DataRequired()])
    place = SelectField('Place', choices=[], validators=[DataRequired()])
    to_edit = IntegerField('To edit')
    to_edit = SelectField('To edit')
    submit = SubmitField('Add / Edit')


class AlbumForm(FlaskForm):
    band = SelectField('Band', choices=[], validators=[DataRequired()])
    name = StringField('Name')
    genre = SelectField('Genre', choices=[], validators=[DataRequired()])
    submit = SubmitField('Add')


class SongForm(FlaskForm):
    name = StringField('Name')
    submit = SubmitField('Add')
