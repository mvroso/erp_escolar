from flask import url_for
from website import mail
from flask_mail import Message

# Send reset email user
def send_reset_email(user):
    token = user.get_reset_token()
    
    msg = Message('Pedido de recuperação de Ssnha',
            sender='noreply@marcusdelboux.com.br', recipients=[user.email])

    msg.body = f"Para recuperar sua senha, clique no link:\n\n" \
            f"{url_for('users.reset_password', token=token, _external=True)}\n\n" \
            f"Se você não fez esse pedido, simplesmente ignore este e-mail."

    mail.send(msg)

# Populate Availability form choices
def get_choices():
    choices = [
        ('09', '09:00 - 10:00'),
        ('10', '10:00 - 11:00'),
        ('11', '11:00 - 12:00'),
        ('12', '12:00 - 13:00'),
        ('13', '13:00 - 14:00'),
        ('14', '14:00 - 15:00'),
        ('15', '15:00 - 16:00'),
        ('16', '16:00 - 17:00'),
        ('17', '17:00 - 18:00'),
    ]
    return choices

# Show weekday names
def get_weekdays():
    weekday_names = [
        'Segunda-feira',
        'Terça-feira',
        'Quarta-feira',
        'Quinta-feira',
        'Sexta-feira',
        'Sábado'
    ]
    return weekday_names