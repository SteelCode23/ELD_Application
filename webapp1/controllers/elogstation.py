from flask import Blueprint, render_template, redirect, url_for, abort
from flask.ext.login import login_required, current_user
from flask.ext.principal import Permission, UserNeed
from flask import Flask, render_template, request
from webapp1.forms import ContactForm
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import time
from bs4 import BeautifulSoup
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import pdb
import bs4
from email import encoders
import json
import base64
from flask_mail import Message, Mail


SCOPES = 'https://mail.google.com//'
CLIENT_SECRET_FILE = '/var/www/html/webapp/client-secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_dir = "/var/www/html/webapp/"
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        # if flags:
        #     credentials = tools.run_flow(flow, store, flags)
        # else:  # Needed only for compatibility with Python 2.6
        #     credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def SendMessage(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print(message['id'])
        return message
    except Exception as e:
        print(e)


def create_message_with_attachment(sender, to, subject, message_text, file):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(message_text)
    message.attach(msg)
    part = MIMEBase('application', "octet-stream")
    print(file)
    part.set_payload(open(file, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="' + str(datetime.datetime.today()) + 'import.xlsx"')
    message.attach(part)
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}


# send a list of files
def create_message_with_attachments(sender, to, subject, message_text, files, names):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(message_text)
    message.attach(msg)
    counter = 0
    for file in files:
        part = MIMEBase('application', "octet-stream")
        print(file)
        part.set_payload(open(file, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="' + names[counter] + '.xlsx"')
        message.attach(part)
        counter = counter + 1
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}


def CreateMessage(sender, to, subject, message_text):
    try:
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes())
    except Exception as e:
        return {'raw': 'raw'}

    raw = raw.decode()
    return {'raw': raw}


elogstation_blueprint = Blueprint(
	'elogstation',
	__name__,
	template_folder='../templates/elogstation',
	url_prefix="/elogstation"
	)


@login_required
@elogstation_blueprint.route('/')
@elogstation_blueprint.route('/<int:page>')
def home(page=1):
    if not current_user.is_authenticated:
        return redirect(url_for('.login_view'))
    return render_template('home.html', page = page)


@login_required
@elogstation_blueprint.route('/home', methods=['GET', 'POST'])
def landingpage(page=1):
    mail = Mail()
    form = ContactForm()
    request.form.get('name')
    request.form.get('email')
    subject = request.form.get('subject')
    if request.method == 'POST':
        if form.validate() == False:
          flash('All fields are required.')
          return render_template('contact.html', form=form)
        else:
          msg = Message(request.form.get('subject'), sender='steel.ricciotti@gmail.com', recipients=['steel.ricciotti@gmail.com'])
          msg.body = request.form.get('message')
          mail.send(msg)
    return render_template('landingpage.html', page = page, form = form)


@elogstation_blueprint.route('/register')
def register():
    return render_template('elogstationexample.html')



@elogstation_blueprint.route('/register2')
def register2():
    return render_template(
        'register2.html'
    )

