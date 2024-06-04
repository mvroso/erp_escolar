import os, secrets
from PIL import Image
from flask import current_app
from datetime import datetime
from random import randrange
from website.models import Status, Origin, Role

# Save user uploaded picture in /static/img/profile_pictures
def save_picture(form_picture, width, height):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,
                'static/img/profile_pictures', picture_fn)
    
    # Resize picture with Pillow
    output_size = (width, height)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn

# Create models list to populate the database
def fetch_models():
    lead_statuses = [
        Status(name='Lead'),
        Status(name='Contato'),
        Status(name='Entrevista'),
        Status(name='Matrícula')
    ]
    
    lead_origins = [
        Origin(name='Site'),
        Origin(name='Telefone'),
        Origin(name='Rede Social'),
        Origin(name='Presencial'),
        Origin(name='Indicação')
    ]

    roles = [
        Role(name='Administrador'),
        Role(name='Auxiliar')
    ]

    return (lead_statuses, lead_origins, roles)

# Create random datetime between two dates
def get_rand_datetime(start_date, end_date):
    random_datetime = str(datetime.fromtimestamp(
                            randrange(round(start_date.timestamp()), 
                                    round(end_date.timestamp()))))
    
    return random_datetime