'''
Docstring for app2

This app deals with jinja templates mostly
'''

# -- IMPORTS
from flask import Flask, url_for, render_template
from flask_bootstrap import Bootstrap5

# -- GLOBALS
app = Flask(__name__)
bootstrap = Bootstrap5(app)

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

@app.route('/putdata')
def putdata():
    return render_template("putdata.html")

@app.route('/getdata')
def getdata():
    return render_template("getdata.html")