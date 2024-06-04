from flask import (Blueprint, render_template, url_for, flash, redirect,
                    request, abort)
from datetime import datetime, date, timedelta
from website import db
from website.models import User, Lead, Status, Origin, History, Meeting
from website.leads.forms import (CreateLeadForm, UpdateLeadForm,
        FilterLeadForm)
from flask_login import current_user, login_required
from sqlalchemy import or_, and_, func

# Declares blueprint
leads = Blueprint('leads', __name__)


# Create a new lead
@leads.route("/lead/create", methods=['GET', 'POST'])
@login_required
def create_lead():
    # initalizes the form
    form = CreateLeadForm()
    
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
                user_id=current_user.id,
                lead_id=lead.id)

            db.session.add(history)
            db.session.commit()

            flash('Sua lead foi criada!', 'success')
            return redirect(url_for('leads.list_lead'))
        else:
            flash('Sua lead não foi criada! Verifique seus inputs', 'danger')
    return render_template('create_update_lead.html', title='Criar Lead', form=form, legend='Criar')


# Show a list of existing leads
@leads.route("/lead/list")
@leads.route("/lead/list/<int:status_id>/<int:origin_id>/<date>/<lead_name>/<email>/<description>/<int:page>")
@login_required
def list_lead(page=1, status_id=0, origin_id=0, date="-", phone="-", lead_name="-", email="-", description="-"):
    # builds the search query
    query = or_(Lead.registered >= datetime.now() - timedelta(days=90))

    if status_id != 0:
        query = and_(query, Lead.status_id == status_id)
    
    if origin_id != 0:
        query = and_(query, Lead.origin_id == origin_id)

    if date != "-":
        query = and_(query, func.date(Lead.registered) == date)

    if lead_name != "-":
        query = and_(query, Lead.name.like("%" + lead_name + "%"))
        
    if email != "-":
        query = and_(query, Lead.email.like('%' + email + '%'))

    if description != "-":
        query = and_(query, Lead.description.like('%' + description + '%'))    
    
    leads = Lead.query.filter(query) \
            .order_by(Lead.registered.desc()) \
            .paginate(page=page, per_page=5)
            
    return render_template('list_lead.html', title='Lista de Leads', 
        leads=leads,
        status_id=status_id, origin_id=origin_id, date=date,
        lead_name=lead_name, email=email, description=description)

# Filter a list of existing leads
@leads.route("/lead/filter", methods=['GET', 'POST'])
@login_required
def filter_lead():
    # initalizes the form
    form = FilterLeadForm()

    if form.validate_on_submit():

        lead_name = form.name.data
        phone = form.phone.data
        email = form.email.data
        description = form.description.data
        date = form.date.data
        
        status_id = form.status.data
        origin_id = form.origin.data

        if date == None:
            date = "-"
        if not lead_name:
            lead_name = "-"
        if not phone:
            phone = "-"
        if not email:
            email = "-"
        if not description:
            description = "-"


        return redirect(url_for('leads.list_lead', status_id=status_id, origin_id=origin_id,
                date=date, lead_name=lead_name, phone=phone, email=email, description=description, page=1))

    return render_template('create_update_lead.html', title='Filtrar Lead', form=form)

# Show details of a single lead
@leads.route("/lead/<int:lead_id>/details")
@login_required
def details_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    history = History.query.filter_by(lead_id=lead_id).all()
    operation = Meeting.query.filter(Meeting.lead_id==lead.id, Meeting.start_time >= date.today() + timedelta(days=1)).first()
    if operation == None:
        operation = "schedule"
    else:
        operation = "update"

    return render_template('details_lead.html', title='Detalhe Lead', operation=operation, lead=lead, history=history)

# Update a single lead
@leads.route("/lead/<int:lead_id>/update", methods=['GET', 'POST'])
@login_required
def update_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    
    # initalizes the form
    form = UpdateLeadForm()
    status_list = [(1, "Lead"), (2, "Contato"),
                        (3, "Entrevista"), (4, "Matrícula")]
    status_list.remove((lead.status.id, lead.status.name))
    status_list.insert(0, (lead.status.id, lead.status.name))
    form.status.choices = status_list
    origin_list = [(1, "Site"), (2, "Telefone"), (3, "Rede Social"),
                        (4, "Presencial"), (5, "Indicação")]
    origin_list.remove((lead.origin.id, lead.origin.name))
    origin_list.insert(0, (lead.origin.id, lead.origin.name))
    form.origin.choices = origin_list

    # update lead in database
    if form.validate_on_submit():
        action = "Alteração de "

        if (lead.name != form.name.data or lead.phone != form.phone.data
            or lead.email != form.email.data or lead.description != form.description.data):
            lead.name = form.name.data
            lead.phone = form.phone.data
            lead.email = form.email.data
            lead.description = form.description.data
            action = action + "Dados / "

        if lead.status.id != int(form.status.data):
            action = action + "Status para " + str(dict(status_list).get(int(form.status.data))) + " / "
            lead.status_id = form.status.data
        
        if lead.origin.id != int(form.origin.data):
            action = action + "Origem para " + str(dict(origin_list).get(int(form.origin.data))) + "  "
            lead.origin_id = form.origin.data

        # create new history row
        history = History(action=action[:-2].strip(),
                registered=datetime.now(),
                user_id=current_user.id,
                lead_id=lead.id)

        db.session.add(history)
        db.session.commit()
        flash('Esse Lead foi alterado com sucesso!', 'success')

        return redirect(url_for('leads.details_lead', lead_id=lead.id))

    # populate form
    elif request.method == 'GET':

        form.name.data = lead.name
        form.phone.data = lead.phone
        form.email.data = lead.email
        form.description.data = lead.description

    return render_template('create_update_lead.html', title='Alterar Lead', form=form, legend='Alterar', lead=lead)


# Delete a single lead
@leads.route("/lead/<int:lead_id>/delete", methods=['POST'])
@login_required
def delete_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    # bulk delete
    History.query.filter_by(lead_id=lead_id).delete()
    Meeting.query.filter_by(lead_id=lead_id).delete()

    db.session.delete(lead)
    db.session.commit()
    
    flash('Esse Lead foi deletado com sucesso!', 'success')
    return redirect(url_for('leads.list_lead'))