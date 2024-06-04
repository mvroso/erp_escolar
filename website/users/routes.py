from flask import Blueprint, render_template, url_for, flash, redirect, request
from website import db, bcrypt
from website.models import User, Availability
from website.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
        RequestResetForm, ResetPasswordForm, AvailabilityForm)
from website.users.utils import send_reset_email, get_choices, get_weekdays
from website.main.utils import save_picture
from flask_login import login_user, logout_user, current_user, login_required
from datetime import time

# Declares blueprint
users = Blueprint('users', __name__)


# Register a new user
@users.route("/register", methods=['GET', 'POST'])
def register():
    # initializes the form
    form = RegistrationForm()

    if request.method == 'POST': 
        if form.validate_on_submit():
            # hashes user password
            hashed_password = bcrypt.generate_password_hash(
                                    form.password.data).decode('utf-8')

            # default role is (2,"Auxiliar")
            role = 2
            if (current_user.is_authenticated and 
                current_user.role.name == "Administrador"):
                role = form.role.data

            user = User(name=form.name.data,
                    email=form.email.data,
                    gender_id=form.gender.data,
                    role_id=role,
                    password=hashed_password)

            db.session.add(user)
            db.session.commit()

            flash('A conta foi criada com sucesso!', 'success')

            if current_user.is_authenticated:
                return redirect(url_for('main.index'))
            else:
                return redirect(url_for('users.login'))

        else:

            flash('Sua conta não foi criada. Verifique seus inputs!', 'danger')

    title = "Registro"
    if current_user.is_authenticated:
        title = "Criar novo usuário"

    return render_template('register.html',
                        title=title, form=form)


# Login user
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:

        flash('Você já está logado!', 'danger')
        return redirect(url_for('main.index'))

    # initializes the form
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(
                            user.password, form.password.data):

            login_user(user, remember=True)
            return redirect(url_for('main.index'))

        else:

            flash('Login sem sucesso. Verifique seu e-mail e senha!', 'danger')
    
    return render_template('login.html', title='Login', form=form)


# Logout user
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))


# Reset password request user
@users.route("/reset_password_request", methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:

        flash('Você já está logado!', 'danger')
        return redirect(url_for('main.index'))

    # initalizes the form
    form = RequestResetForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)

        flash('Um e-mail foi enviado com instruções para recuperar sua senha', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_password_request.html', title='Pedido de recuperação de senha', form=form)


# Reset password user
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:

        flash('Você já está logado!', 'danger')
        return redirect(url_for('main.index'))

    user = User.verify_reset_token(token)

    if user is None:

        flash('O token é inválido ou está expirado', 'warning')
        return redirect(url_for('users.reset_password_request'))

    # initializes the form
    form = ResetPasswordForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password

        db.session.commit()

        flash('A sua senha foi alterada!', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_password.html', title='Recuperar senha', form=form)


# Show current user account
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    # initializes the form
    form = UpdateAccountForm()

    if form.validate_on_submit():
        # saves picture image and hash
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 200, 200)
            current_user.image_file = picture_file

        current_user.name = form.name.data
        current_user.email = form.email.data

        db.session.commit()

        flash('Seus dados foram alterados!', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':

        form.name.data = current_user.name
        form.email.data = current_user.email

    # Get current user profile picture
    image_file = url_for('static', filename='img/profile_pictures/' +
                        current_user.image_file)

    return render_template('account.html', title='Conta',
                        image_file=image_file, form=form)


# Setup user availability
@users.route("/availability/setup", methods=['GET', 'POST'])
@login_required
def setup_availability():
    # initalizes the form
    form = AvailabilityForm()

    # set choices for weekday selects
    for select in form.weekdays:
        select.available_timeslot.choices = get_choices()
    form.saturday.available_timeslot.choices = get_choices()

    if request.method == 'GET':
        previous_availability = Availability.query.filter_by(user_id=current_user.id)
        selected_options = []
        for timeslot in previous_availability:
            selected_options.append([timeslot.weekday, timeslot.start_time.strftime("%H")])
        # opening hours
        weekday_disabled_options = ['13']
        saturday_disabled_options = ['13', '14', '15', '16', '17']

    elif request.method == 'POST':
        if form.validate_on_submit():
            # delete previous availability
            Availability.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            availability = []
            for index, select in enumerate(form.weekdays):
                for start_time in select.available_timeslot.data:
                    availability.append(Availability(weekday=index, # monday start
                        start_time = time(int(start_time)),
                        user_id = current_user.id))
            for start_time in form.saturday.available_timeslot.data:
                    availability.append(Availability(weekday=5, # monday start
                        start_time = time(int(start_time)),
                        user_id = current_user.id))
            db.session.add_all(availability)
            db.session.commit()           

            flash('Sua disponibilidade foi configurada!', 'success')
            return redirect(url_for('users.setup_availability'))
        else:
            flash('Verifique seus inputs', 'danger')
    return render_template('setup_availability.html', title='Configurar Disponibilidade', form=form,
                selected_options=selected_options, weekday_disabled_options=weekday_disabled_options,
                saturday_disabled_options=saturday_disabled_options, weekday_names=get_weekdays(), legend='Configurar')