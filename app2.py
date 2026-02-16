'''
Docstring for app2

This app deals with jinja templates mostly
'''

# -- IMPORTS
from hashlib import sha256
from datetime import datetime, timedelta
import os

from flask import Flask, url_for, render_template, redirect, request
from flask_bootstrap import Bootstrap5

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length

# -- GLOBALS
db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = '?kndeu8n3nw9e9e8dn3983e!'

bootstrap = Bootstrap5(app) # init bootstrap

csrf = CSRFProtect(app) # for WTF

db_name = 'invoices.db'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, db_name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

# -- Classes
class DataEntryForm(FlaskForm):
    def_today = datetime.today()
    def_target = datetime.today() + timedelta(days=14)

    inv_patient = SelectField('Invoice Patient',
                              choices=['Annika','Thomas','Luise','Janusz','Clemens'],
                              validators=[DataRequired()])
    inv_date = DateField('Invoice Date', 
                         format="%Y-%m-%d",
                         default=def_today,
                         validators=[DataRequired()])
    inv_id = StringField('Invoice ID', validators=[DataRequired()])
    inv_name = StringField('Invoice Name', validators=[DataRequired()])
    inv_value = StringField('Invoice Value', validators=[DataRequired()])
    inv_paydate = DateField('Invoice Payment Target',
                            format="%Y-%m-%d",
                            default=def_target,
                            validators=[DataRequired()])
    submit = SubmitField('Submit')

class Invoices(db.Model):
    __tablename__ = 'invoices'
    N = db.Column(db.Integer, primary_key=True)
    HASH = db.Column(db.String)
    DATE = db.Column(db.String)
    ID = db.Column(db.String)
    NAME = db.Column(db.String)
    VALUE = db.Column(db.String)
    PAYDATE = db.Column(db.String)
    PATIENT = db.Column(db.String)
    def __init__(self, HASH, DATE, ID, NAME, VALUE, PAYDATE, PATIENT):
        #self.N = N
        self.HASH = HASH
        self.DATE = DATE
        self.ID = ID
        self.NAME = NAME
        self.VALUE = VALUE
        self.PAYDATE = PAYDATE
        self.PATIENT = PATIENT

# -- Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/image')
def image():
    return render_template("image.html")

@app.route('/putdata', methods=['GET', 'POST'])
def putdata():
    message = ""
    form = DataEntryForm()
    if form.validate_on_submit():
        inv_patient = request.form['inv_patient']
        inv_date = request.form['inv_date']
        inv_id = request.form['inv_id']
        inv_name = request.form['inv_name']
        inv_value = request.form['inv_value']
        inv_paydate = request.form['inv_paydate']
        rawhash = sha256()
        rawhash.update(str(inv_date).encode('utf8'))
        rawhash.update(str(inv_patient).encode('utf8'))
        rawhash.update(str(inv_id).encode('utf8'))
        rawhash.update(str(inv_name).encode('utf8'))
        rawhash.update(str(inv_value).encode('utf8'))
        rawhash.update(str(inv_paydate).encode('utf8'))
        entry_hash = rawhash.hexdigest()
        record = Invoices(entry_hash[0:11],
                          inv_date,
                          inv_id,
                          inv_name,
                          inv_value,
                          inv_paydate,
                          inv_patient)#HASH, DATE, ID, NAME, VALUE, PAYDATE, PATIENT)
        db.session.add(record)
        db.session.commit()
        # create a message to send to the template
        message = f"NEW DATA has been submitted."
    return render_template("putdata.html", form=form, message=message)

@app.route('/getdata')
def getdata():
    invoices = db.session.execute(db.select(Invoices).order_by(Invoices.N)).scalars()
    return render_template("getdata.html", invoices=invoices)