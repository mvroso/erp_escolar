from flask import (Blueprint, render_template, url_for, flash, redirect,
                    request, abort)
from datetime import datetime, date, time, timedelta
from website import db
from website.models import User, Lead, Status, Origin, History, Meeting, Availability
from website.meetings.forms import (ScheduleMeetingForm)#, UpdateMeetingForm,
        #FilterMeetingForm)
from website.meetings.utils import get_choices, get_weekdays, get_next_working_days
from flask_login import current_user, login_required
from sqlalchemy import or_, and_, func

# Declares blueprint
meetings = Blueprint('meetings', __name__)

# Schedule a new meeting or Update a single meeting
@meetings.route("/meeting/<operation>/<int:lead_id>/<int:user_id>", methods=['GET', 'POST'])
def schedule_update_meeting(operation, lead_id, user_id):
    lead = Lead.query.get_or_404(lead_id)
    user = User.query.get_or_404(user_id)
    title = "Marcar Reunião"
    action = "Reunião marcada para "

    # initalizes the form
    form = ScheduleMeetingForm()
    for select in form.weekdays:
            select.available_timeslot.choices = get_choices()

    # get previous meeting time
    previous_start_time = None
    previous_date = None
    previous_time = None
    check_update = Meeting.query.filter(Meeting.lead_id==lead.id, Meeting.start_time > datetime.now()).first()
    
    if operation == "update":
        title = "Remarcar Reunião"
        action = "Reunião remarcada para "

    # check what's the availability for the next 6 days
    next_dates = get_next_working_days(date.today() + timedelta(days=1), 6)
    weekday_names = get_weekdays()
    
    if request.method == 'GET':
        if check_update is not None:
            previous_start_time = check_update.start_time
            previous_date = previous_start_time.date()
            previous_time = previous_start_time.strftime("%H")
            form.description.data = check_update.description

        all_available_timeslots = []
        for working_day in next_dates:
            # builds the search query
            availabilities = Availability.query.filter_by(user_id=user.id,
                                                weekday=working_day.weekday()
                                                ).all()
            meetings = Meeting.query.filter(Meeting.user_id==user.id,
                                        Meeting.start_time.between(
                                            datetime.combine(working_day, time.min),
                                            datetime.combine(working_day, time.max))
                                        ).all()

            available_timeslots = []
            for timeslot in availabilities:
                available_timeslots.append(timeslot.start_time.strftime("%H"))

            for meeting in meetings:
                if (meeting.start_time.strftime("%H") in available_timeslots
                    and meeting.start_time != previous_start_time):
                    available_timeslots.remove(meeting.start_time.strftime("%H"))

            all_available_timeslots.append([working_day, weekday_names[working_day.weekday()], available_timeslots])

    elif request.method == 'POST':
        if form.validate_on_submit():
            if operation == "update":
                # delete previous meeting
                Meeting.query.filter(Meeting.lead_id == lead.id, Meeting.start_time >= datetime.now()).delete()
                db.session.commit()
            for select in form.weekdays:
                weekday_num = int(select.available_timeslot.name.split('-')[1]) # get date from current select id
                for start_time in select.available_timeslot.data:
                    meeting = Meeting(start_time = datetime.combine(next_dates[weekday_num], time(int(start_time))),
                        description = form.description.data,
                        user_id = user.id,
                        lead_id = lead.id)
                    history = History(action=(action + next_dates[weekday_num].strftime('%d/%m') + " às " + start_time + " horas" ),
                        registered=datetime.now(),
                        user_id=user.id,
                        lead_id=lead.id)

            db.session.add(meeting)
            db.session.add(history)
            db.session.commit()

            flash('Sua reunião foi marcada!', 'success')
            return redirect(url_for('meetings.list_meeting'))
        else:
            flash('Sua reunião não foi marcada! Verifique seus inputs', 'danger')
    return render_template('schedule_update_meeting.html', title=title, form=form, legend='Marcar', lead=lead, operation=operation,
            all_available_timeslots=all_available_timeslots, previous_date=previous_date, previous_time=previous_time)

# Delete a single meeting
@meetings.route("/meeting/delete/<int:lead_id>", methods=['POST'])
def delete_meeting(lead_id):
    meeting = Meeting.query.filter(Meeting.lead_id==lead_id, Meeting.start_time >= datetime.now()).first()
    history = History(action=("Reunião desmarcada"),
                        registered=datetime.now(),
                        user_id=current_user.id,
                        lead_id=lead.id)

    db.session.delete(meeting)
    db.session.add(history)
    db.session.commit()

    flash('Reunião desmarcada com sucesso!', 'success')
    return redirect(url_for('leads.list_lead'))

# Show a list of existing meetings
@meetings.route("/meeting/list")
@login_required
def list_meeting():
    # builds the search query
    query = or_(Meeting.start_time >= datetime.now())
    if current_user.role.name == "Auxiliar":
        query = and_(query, Meeting.user_id == current_user.id)

    meetings = Meeting.query.filter(query) \
            .order_by(Meeting.start_time.asc()).all()

    headings = []
    for index, meeting in enumerate(meetings):
        if index == 0:
            headings.append(True)
            date_check = meeting.start_time.strftime("%d/%m/%y")
        else:
            if meeting.start_time.strftime("%d/%m/%y") != date_check:
                headings.append(True)
                date_check = meeting.start_time.strftime("%d/%m/%y")
            else:
                headings.append(False)

    return render_template('list_meeting.html', title='Lista de Reuniões', 
        meetings=meetings, headings=headings)