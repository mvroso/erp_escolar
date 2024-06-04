from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from website import db, login_manager
from flask import current_app
from flask_login import UserMixin

# Decorator - session user loading (Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User class extends UserMixin (Flask-Login)
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # choices (Masculino = 1, Feminino = 2, Não se aplica = 3)
    gender_id = db.Column(db.Integer, nullable=False, default=1)

    # user image hash
    image_file = db.Column(db.String(30), nullable=False, default='default.jpg')

    # foreign key = Role (Administrador = 1, Auxiliar = 2)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=2)

    # relationship = User | one to Many | History
    history = db.relationship('History', backref='user', lazy=True)

    # relationship = User | one to Many | Availability
    availability = db.relationship('Availability', backref='user', lazy=True)

    # relationship = User | one to Many | Meeting
    meeting = db.relationship('Meeting', backref='user', lazy=True)

    # generate a reset password token that expires in 10 minutes
    def get_reset_token(self, expires_sec=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # verifies the reset password token and returns the user_id or None
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}', '{self.role.name}')"

# Role class (user permissions)
class Role(db.Model):
    __tablename__ = 'role'

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(30), unique=True, nullable=False)

    # relationship = Role | one to Many | User
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return f"Role('{self.id}', '{self.name}')"


# Availability class (user schedule)
class Availability(db.Model):
    __tablename__ = 'availability'

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    weekday = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)

    # foreign key = User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Availability('{self.id}')"

# Meeting class
class Meeting(db.Model):
    __tablename__ = 'meeting'

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    start_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # foreign key = Lead
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=False)

    # foreign key = User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Meeting('{self.id}')"

# Status class
class Status(db.Model):
    __tablename__ = 'status'

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(30), unique=True, nullable=False)

    # relationship = Status | one to Many | Lead
    statuses = db.relationship('Lead', backref='status', lazy=True)

    def __repr__(self):
        return f"Status('{self.id}', '{self.name}')"

# Origin class
class Origin(db.Model):
    __tablename__ = 'origin'

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(30), unique=True, nullable=False)

    # relationship = Origin | one to Many | Lead
    origins = db.relationship('Lead', backref='origin', lazy=True)

    def __repr__(self):
        return f"Origin('{self.id}', '{self.name}')"

# Lead class
class Lead(db.Model):
    __tablename__ = 'lead'

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # foreign key = Status (Lead = 1, Contato = 2, Entrevista = 3, Matrícula = 4)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False, default=1)

    # foreign key = Origin (Site = 1, Telefone = 2, Rede Social = 3, Presencial = 4, Indicação = 5)
    origin_id = db.Column(db.Integer, db.ForeignKey('origin.id'), nullable=False, default=1)

    # relationship = Lead | one to Many | History
    history = db.relationship('History', backref='lead', lazy=True)

    # relationship = Lead | one to Many | Meeting
    meeting = db.relationship('Meeting', backref='lead', lazy=True)

    def __repr__(self):
        return f"Lead('{self.name}')"

# History class (lead interactions)
class History(db.Model):
    __tablename__ = 'history'

    # primary key
    id = db.Column(db.Integer, primary_key=True)

    action = db.Column(db.String(100), nullable=False)
    registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # foreign key = Lead
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=False)

    # foreign key = User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"History('{self.id}', '{self.name}')"
