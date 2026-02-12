'''
Docstring for app2

This app deals with jinja templates mostly
'''

# -- IMPORTS
from flask import Flask, url_for, render_template

# -- GLOBALS
app = Flask(__name__)

# -- Routes
@app.route('/')
def index():
    return render_template("index.html")