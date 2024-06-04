from datetime import date as date_func
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, DateField, TextAreaField,
		SelectField, IntegerField, EmailField)
from wtforms.validators import (DataRequired, Length, ValidationError,
		Optional, NumberRange, Email, Regexp)

# Mixin for create and update lead
class LeadFormMixin():

	name = StringField('Nome',
					validators=[DataRequired(), Length(min=2, max=50)])

	phone = StringField('Telefone',
					validators=[DataRequired()])

	email = EmailField('Endereço de e-mail',
				validators=[DataRequired(), Email()])

	description = TextAreaField('Descrição')

	status = SelectField('Status',
				validators=[DataRequired()],
				choices=[(1, "Lead"), (2, "Contato"),
						(3, "Entrevista"), (4, "Matrícula")])

	origin = SelectField('Origem',
				validators=[DataRequired()],
				choices=[(1, "Site"), (2, "Telefone"), (3, "Rede Social"),
						(4, "Presencial"), (5, "Indicação")])

# Create lead form extends LeadFormMixin
class CreateLeadForm(FlaskForm, LeadFormMixin):

    submit = SubmitField('Criar Lead')


# Update lead form extends LeadFormMixin
class UpdateLeadForm(FlaskForm, LeadFormMixin):

    submit = SubmitField('Alterar Lead')


# Filter lead Form
class FilterLeadForm(FlaskForm):


	name = StringField('Nome',
					validators=[Optional()])

	email = EmailField('Endereço de e-mail',
				validators=[Optional(), Email()])

	phone = StringField('Telefone',
					validators=[Optional()])

	description = TextAreaField('Descrição',
					validators=[Optional()])

	date = DateField('Data de criação', format='%Y-%m-%d',
					validators=[Optional()])

	status = SelectField('Status',
				validators=[Optional()],
				choices=[(0, "Qualquer Status"), (1, "Lead"), (2, "Contato"),
                        (3, "Entrevista"), (4, "Matrícula")])

	origin = SelectField('Origem',
				validators=[Optional()],
				choices=[(0, "Qualquer Origem"), (1, "Site"), (2, "Telefone"),
                        (3, "Rede Social"), (4, "Presencial"), (5, "Indicação")])

	submit = SubmitField('Filtrar Lead')