from flask import Flask
# Database management
from flask_sqlalchemy import SQLAlchemy
# Cryptography for storing hashes
from flask_bcrypt import Bcrypt
# User session management
from flask_login import LoginManager
# Mail management
from flask_mail import Mail
# Configuration
from website.config import Config

# Flask-SQLAlchemy
db = SQLAlchemy()
# Flask-Bcrypt
bcrypt = Bcrypt()
# Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
# Flask-Mail
mail = Mail()


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	# Initializing extensions
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	# Initializing blueprints
	from website.main.routes import main
	from website.leads.routes import leads
	from website.meetings.routes import meetings
	from website.users.routes import users
	from website.errors.handlers import errors
	app.register_blueprint(main)
	app.register_blueprint(leads)
	app.register_blueprint(meetings)
	app.register_blueprint(users)
	app.register_blueprint(errors)

	return app