from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, SubmitField, EmailField,
		SelectField, SelectMultipleField, FieldList, FormField)
from wtforms.validators import (DataRequired, Length, EqualTo, Email,
		ValidationError, Optional)
from flask_login import current_user
from website.models import User

# User registration form
class RegistrationForm(FlaskForm):
	name = StringField('Nome',
				validators=[DataRequired(), Length(min=2, max=50)])

	email = EmailField('Endereço de e-mail',
				validators=[DataRequired(), Email()])

	gender = SelectField('Gênero',
				validators=[DataRequired()],
				choices=[(1, "Masculino"), (2, "Feminino"),
						(3, "Não se aplica")])

	role = SelectField('Tipo',
				validators=[Optional()],
				choices=[(1, "Administrador"), (2, "Auxiliar")])

	password = PasswordField('Senha',
				validators=[DataRequired()])

	confirm_password = PasswordField('Confirme sua senha',
				validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Criar usuário')

	# email validation
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Esse e-mail já está em uso')

# Login User form
class LoginForm(FlaskForm):
	email = StringField('E-mail',
				validators=[DataRequired(), Email()])

	password = PasswordField('Senha',
				validators=[DataRequired()])

	submit = SubmitField('Login')

# Request reset password User form
class RequestResetForm(FlaskForm):
	email = StringField('E-mail',
				validators=[DataRequired(), Email()])

	submit = SubmitField('Recuperar Senha')

	# email validation
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('Este e-mail não está vinculado a nenhuma conta')

# Reset password User form
class ResetPasswordForm(FlaskForm):
	password = PasswordField('Nova senha',
				validators=[DataRequired()])

	confirm_password = PasswordField('Confirme a nova senha',
				validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Recuperar Senha')

# Update User form
class UpdateAccountForm(FlaskForm):
	name = StringField('Nome',
				validators=[DataRequired(), Length(min=2, max=50)])

	email = EmailField('Endereço de e-mail',
				validators=[DataRequired(), Email()])

	picture = FileField('Foto de perfil',
					validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

	submit = SubmitField('Alterar')

	# email validation
	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Este e-mail já está em uso')

# Available Time select form
class AvailableTimeSelectForm(Form):
    available_timeslot = SelectMultipleField('Horários disponíveis',
    					validators=[Optional()], choices=[])

# User availability form
class AvailabilityForm(FlaskForm):
    weekdays = FieldList(FormField(AvailableTimeSelectForm), min_entries=5)
    saturday = FormField(AvailableTimeSelectForm)

    submit = SubmitField('Cadastrar horários disponíveis')