from flask import Blueprint, render_template

# Declares blueprint
main = Blueprint('main', __name__)


# Show index page
@main.route("/")
@main.route("/index")
def index():
    return render_template('index.html', title='Home')


# Imports for inserting data
from flask import flash, redirect, url_for, request, abort
from flask_login import current_user
from datetime import datetime, date, time, timedelta
from lorem_text import lorem
import random
from random import randint
from website import db, bcrypt
from website.models import User, Lead, History, Availability, Meeting
from website.main.utils import fetch_models, get_rand_datetime
from website.meetings.utils import get_next_working_days
from website.leads.forms import CreateLeadForm

# Show contact page
@main.route("/contact", methods=['GET', 'POST'])
def contact():
    if current_user.is_authenticated:
        flash('Somente usuários não logados!', 'danger')
        abort(403) # 403 = forbidden access
    
    # initalizes the form
    form = CreateLeadForm(status=1)
    
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        if form.validate_on_submit():

            creation_time = datetime.now()

            lead = Lead(name=form.name.data,
                phone=form.phone.data,
                email=form.email.data,
                description=form.description.data,
                registered=creation_time,
                status_id=form.status.data,
                origin_id=form.origin.data)

            db.session.add(lead)
            db.session.commit()

            history = History(action="Lead criado",
                registered=creation_time,
                user_id=None,
                lead_id=lead.id)

            db.session.add(history)
            db.session.commit()

            flash('Entraremos em contato assim que possível!', 'success')
            return redirect(url_for('main.contact'))
        else:
            flash('Por favor, verifique seus inputs', 'danger')
    
    return render_template('contact.html', title='Contato', form=form, legend='Create')

# Populate the database for the first time with necessary and dummy data
@main.route("/insertdata")
def insertdata():

    (lead_statuses, lead_origins, roles) = fetch_models()

    # create four lead statuses
    db.session.add_all(lead_statuses)
    db.session.commit()

    # create five lead origins
    db.session.add_all(lead_origins)
    db.session.commit()  

    # create two roles
    db.session.add_all(roles)
    db.session.commit()

    # create 10 standard users
    hashed_password = bcrypt.generate_password_hash(
                                    "1234").decode('utf-8')

    users = [
        User(name='Teste da Silva',
                email='teste@teste.com',
                password=hashed_password,
                gender_id=2),
        User(name='Agenore Bruno',
                email='agenorebruno@teste.com',
                password=hashed_password,
                gender_id=1),
        User(name='Amalio Davide',
                email='amaliodavide@teste.com',
                password=hashed_password,
                gender_id=1),
        User(name='Sandra Romani',
                email='sandraromani@teste.com',
                password=hashed_password,
                gender_id=3),
        User(name='Maria Pia Udinese',
                email='mariapiaudinese@teste.com',
                password=hashed_password,
                gender_id=2),
        User(name='Ornella Lettiere',
                email='ornellalettiere@teste.com',
                password=hashed_password,
                gender_id=2),
        User(name='Bernardo Genovesi',
                email='bernardogenovesi@teste.com',
                password=hashed_password,
                gender_id=1),
        User(name='Matteo Cattaneo',
                email='matteocattaneo@teste.com',
                password=hashed_password,
                gender_id=1),
        User(name='Antonio Greece',
                email='antoniogreece@teste.com',
                password=hashed_password,
                gender_id=3),
        User(name='Raffaele Lombardi',
                email='raffaelelombardi@teste.com',
                password=hashed_password,
                gender_id=1)
    ]
    db.session.add_all(users)
    db.session.commit()

    # create 1 administrator user
    administrator = User(name='Administrador',
                email='admin@teste.com',
                password=hashed_password,
                gender_id=1,
                role_id=1)
    
    db.session.add(administrator)
    db.session.commit()
    
    # create 20 standard leads
    start_date = datetime(2024, 5, 20)
    end_date = datetime(2024, 6, 21)
    registered_list = [get_rand_datetime(start_date, end_date)
                        for i in range(20)]
    word_number = 10

    leads = [
        Lead(name='Lorena Gabrielly',
                phone='5573982094195',
                email='lorena-peixoto74@brasildakar.com.br',
                description=lorem.words(word_number),
                registered=registered_list[0],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Diego Isaac Daniel',
                phone='5581996439093',
                email='diego_galvao@emayl.com',
                description=lorem.words(word_number),
                registered=registered_list[1],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Benjamin Thiago Murilo',
                phone='5583983656956',
                email='benjamin_melo@acramisper.com',
                description=lorem.words(word_number),
                registered=registered_list[2],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Manoel Raul Cardoso',
                phone='5591998368434',
                email='manoel-cardoso85@callan.com.br',
                description=lorem.words(word_number),
                registered=registered_list[3],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Helena Jéssica Bernardes',
                phone='5561982403024',
                email='helena_jessica_bernardes@l3ambiental.com.br',
                description=lorem.words(word_number),
                registered=registered_list[4],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='João Marcos Vinicius Enrico',
                phone='5584995238764',
                email='joao_marcos_fernandes@gerj.com.br',
                description=lorem.words(word_number),
                registered=registered_list[5],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Joaquim Cauê das Neves',
                phone='5567997224686',
                email='joaquim.caue.dasneves@protenisbarra.com.br',
                description=lorem.words(word_number),
                registered=registered_list[6],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Olivia Eloá Vieira',
                phone='5583984544170',
                email='oliviaeloavieira@uolinc.com',
                description=lorem.words(word_number),
                registered=registered_list[7],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Bruna Jennifer Carolina Barros',
                phone='5577998444191',
                email='bruna_jennifer_barros@jci.com',
                description=lorem.words(word_number),
                registered=registered_list[8],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Vinicius Gael da Silva',
                phone='5598999683795',
                email='vinicius.gael.dasilva@piemme.com.br',
                description=lorem.words(word_number),
                registered=registered_list[9],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Noah Tomás Novaes',
                phone='5511991185655',
                email='noah_tomas_novaes@sefaz.am.gov.br',
                description=lorem.words(word_number),
                registered=registered_list[10],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Camila Olivia Silvana',
                phone='5566983755255',
                email='camila_olivia_oliveira@alesalvatori.com',
                description=lorem.words(word_number),
                registered=registered_list[11],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Cecília Evelyn Joana',
                phone='5584983374432',
                email='cecilia_freitas@arcante.com.br',
                description=lorem.words(word_number),
                registered=registered_list[12],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Marcela Marina Campos',
                phone='5521995958710',
                email='marcela_marina_campos@asconnet.com.br',
                description=lorem.words(word_number),
                registered=registered_list[13],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Enrico Elias Mendes',
                phone='5551987508226',
                email='enrico.elias.mendes@gmail.com.br',
                description=lorem.words(word_number),
                registered=registered_list[14],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Nair Alícia Drumond',
                phone='5588998856713',
                email='nair-drumond71@almaquinas.com.br',
                description=lorem.words(word_number),
                registered=registered_list[15],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Catarina Julia',
                phone='5533998671431',
                email='catarina-damota73@yahoo.com.br',
                description=lorem.words(word_number),
                registered=registered_list[16],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Severino Mateus Gomes',
                phone='5573987058911',
                email='severinomateusgomes@yahoo.com.br',
                description=lorem.words(word_number),
                registered=registered_list[17],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Paulo Aparício',
                phone='5511992605234',
                email='paulo-aparicio73@lynce.com.br',
                description=lorem.words(word_number),
                registered=registered_list[18],
                status_id=randint(1,4),
                origin_id=randint(1,5)),
        Lead(name='Rafael da Rosa',
                phone='5565983867315',
                email='rafael_darosa@transicao.com',
                description=lorem.words(word_number),
                registered=registered_list[19],
                status_id=randint(1,4),
                origin_id=randint(1,5))
    ]

    db.session.add_all(leads)
    db.session.commit()

    # create 20 correspondant history inputs
    history = []
    for index in range(20):
        history.append(History(action="Lead criado",
                registered=registered_list[index],
                user_id=randint(1,11),
                lead_id=(index+1)))

    db.session.add_all(history)
    db.session.commit()

    # setup availability for users (4 random timeslots)
    availability = []
    for user in users:
        for index in range(6):
            available_timeslots = [9, 10, 11, 12, 14, 15, 16, 17]
            for index_inter in range(4):
                if index == 4: # saturday
                    choice = random.choice(available_timeslots[:4])
                else:
                    choice = random.choice(available_timeslots)
                availability.append(Availability(weekday=index, # monday start
                    start_time = time(choice),
                    user_id = user.id))
                available_timeslots.remove(choice)
    
    db.session.add_all(availability)
    db.session.commit()
    
    # setup meetings for users and leads and create correspondant history inputs
    working_days = get_next_working_days(date.today() + timedelta(days=1), 5)
    meetings = []
    history = []
    user_ids = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    lead_ids = ['1', '3', '6', '7', '8', '10', '12', '15', '17', '18']
    for index in range(10): # 12 meetings
        user_choice = random.choice(user_ids)
        lead_choice = random.choice(lead_ids)
        user_ids.remove(user_choice)
        lead_ids.remove(lead_choice)

        available_timeslots = []
        availabilities = Availability.query.filter_by(user_id=user_choice,
                                        weekday=working_days[index % 5].weekday()
                                        ).all()

        for timeslot in availabilities:
                available_timeslots.append(timeslot.start_time.strftime("%H"))

        timeslot_choice = int(random.choice(available_timeslots))

        meetings.append(Meeting(start_time = datetime.combine(working_days[index % 5],
                                        time(timeslot_choice)),
                                description=lorem.words(word_number),
                                lead_id = lead_choice,
                                user_id = user_choice))

        history.append(History(action="Reunião marcada",
                lead_id=lead_choice,
                user_id=user_choice))
    
    db.session.add_all(meetings)
    db.session.commit()

    db.session.add_all(history)
    db.session.commit()
    
    flash('O banco de dados foi populado com dummy data', 'info')
    return redirect(url_for('main.index'))