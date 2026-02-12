'''
Docstring for app

This app follows the flask quick start guide
'''

# IMPORTS
from flask import Flask, request
from markupsafe import escape

# GLOBALS
app = Flask(__name__)

# Routes
@app.route("/")
def helloworld():
    return "<h1>HELLO WONDERFUL WORLD!</h1>"

@app.route("/hello")
def hello():
    name = request.args.get("name", "Flask")
    return f"Hello, {escape(name)}!"