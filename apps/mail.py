from flask_mail import Mail, Message
from flask import render_template
import os


mail_config = {
    'MAIL_SERVER': 'smtp.gmail.com', 
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USERNAME': os.environ.get('MAIL_USERNAME'),
    'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD'),
    'FLASK_MAIL_SENDER': f"for.mailing.shop <{os.environ.get('MAIL_USERNAME')}>", 
}

mail = Mail()


def send_order_add_email(client, sum, order_list):
    msg = Message('Ваш заказ', sender=mail_config['FLASK_MAIL_SENDER'], recipients=[client.email])
    #msg.html = f"""<h2>Здравствуйте, {client.name}!</h2>\n<h3>Вы оформили заказ на сумма {sum} рублей.</h3>"""
    msg.html = render_template('mail/send_order_add_email.html', client=client, sum=sum, order_list=order_list)
    mail.send(msg)
