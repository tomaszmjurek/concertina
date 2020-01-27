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
    formation_date = DateField('Formation date', default=None)
    to_edit = SelectField('Id/Name to edit')
    submit = SubmitField('Add / Edit')


class MusicianForm(FlaskForm):
    name = StringField('Name')
    band = SelectField('Band', choices=[], validators=[DataRequired()])
    instrument = SelectField('Instrument', choices=[], validators=[DataRequired()])
    nationality = StringField('Nationality')
    to_edit = SelectField('Id/Name to edit')
    submit = SubmitField('Add / Edit')


class FestivalForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date_start = DateField('Start date', validators=[DataRequired()])
    place = SelectField('Place', choices=[], validators=[DataRequired()])
    to_edit = SelectField('Id/Name to edit')
    submit = SubmitField('Add / Edit')


class AlbumForm(FlaskForm):
    band = SelectField('Band', choices=[], validators=[DataRequired()])
    name = StringField('Name')
    genre = SelectField('Genre', choices=[], validators=[DataRequired()])
    to_edit = SelectField('Id/Name to edit')
    submit = SubmitField('Add / Edit')


class SongForm(FlaskForm):
    name = StringField('Name')
    position = IntegerField('Position')
    length = IntegerField('Length [s]')
    to_edit = SelectField('Id/Name to edit')
    submit = SubmitField('Add / Edit')


class InstrumentForm(FlaskForm):
    type = StringField('Instrument type')
    to_edit = SelectField('Id/Name to edit')
    submit = SubmitField('Add / Edit')


class QueryForm(FlaskForm):
    query = StringField('Query')
    submit = SubmitField('Search')


class ConcertsQueryForm(FlaskForm):
    days = IntegerField('Days')
    query = StringField('Query')
    submit = SubmitField('Search')


class PlaceForm(FlaskForm):
    name = StringField('Name')
    city = StringField('City')
    street = StringField('Street')
    to_edit = SelectField('Id/Name to edit')
    submit = SubmitField('Add / Edit')


class GenreForm(FlaskForm):
    name = StringField('Name')
    supergenre = SelectField('Supergenre', choices=[])
    to_edit = SelectField('Id/Name to edit')
    submit = SubmitField('Add / Edit')


class AwardForm(FlaskForm):
    name = StringField('Name')
    to_edit = SelectField('Id/Name to edit')
    submit = SubmitField('Add / Edit')


class AwardReceptionForm(FlaskForm):
    album = SelectField('Album', choices=[], validators=[DataRequired()])
    submit = SubmitField('Add')


class AppearanceForm(FlaskForm):
    band = SelectField('Band', choices=[], validators=[DataRequired()])
    submit = SubmitField('Add')