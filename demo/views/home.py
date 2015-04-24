# -*- coding: utf-8 -*-
# from ghiro import app
from jinja2 import TemplateNotFound
from flask import Blueprint, render_template, abort, current_app
from datetime import datetime
from demo.database import engine

mod = Blueprint('home', __name__)


@mod.route('/')
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)
