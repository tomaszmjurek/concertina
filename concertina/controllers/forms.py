from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from datetime import date


class ConcertForm(FlaskForm):
    band = SelectField('Band', choices=[], validators=[DataRequired()])
    place = SelectField('Place', choices=[], validators=[DataRequired()])
    concert_date = DateField('Concert date', validators=[DataRequired()], default=date.today())
    tour = StringField('Tour')
    submit = SubmitField('Add')


class BandForm(FlaskForm):
    name = StringField('Name') # warunek, nie ma juz takiego
    formation_date = DateField('Formation date', default=date.today())
    submit = SubmitField('Add')
