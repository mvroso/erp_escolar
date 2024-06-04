from datetime import date as date_func
from flask_wtf import FlaskForm, Form
from wtforms import (StringField, SubmitField, DateField, TextAreaField,
		SelectField, SelectMultipleField, IntegerField, EmailField, DateField,
		FieldList, FormField)
from wtforms.validators import (DataRequired, Length, ValidationError,
		Optional, NumberRange, Email, Regexp)

# Available Time select form
class AvailableTimeSelectForm(Form):
    available_timeslot = SelectMultipleField('Horários disponíveis',
    					validators=[Optional()], choices=[])

# User availability form
class ScheduleMeetingForm(FlaskForm):
    weekdays = FieldList(FormField(AvailableTimeSelectForm),
    						min_entries=6)
    description = TextAreaField('Comentários',
							validators=[Optional()])

    submit = SubmitField('Marcar reunião')