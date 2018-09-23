from datetime import datetime
from flask import url_for
from . import main

@main.route('/', methods=['GET', 'POST'])
def index():
    return '<h1>Hello, World!</h1>'
