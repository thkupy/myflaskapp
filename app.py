'''
Docstring for app

This app follows the flask quick start guide
'''

# -- IMPORTS
from flask import Flask, request
from markupsafe import escape

# -- GLOBALS
app = Flask(__name__)

# -- Routes
# most basic: return html
@app.route('/')
def helloworld():
    return "<h1>HELLO WONDERFUL WORLD!</h1>"

# requests sanitizes parameters
@app.route('/hello')
def hello():
    name = request.args.get("name", "Flask")
    return f"Hello, {escape(name)}!"

# variable routes
@app.route('/user/<username>')
def show_user_profile(username):
    return f"User {escape(username)}"

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f"Post {post_id}"