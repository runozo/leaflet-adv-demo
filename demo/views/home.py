# -*- coding: utf-8 -*-
# from ghiro import app
from jinja2 import TemplateNotFound
from flask import Blueprint, render_template, abort, current_app, request, jsonify
from datetime import datetime
# from demo.database import engine

mod = Blueprint('home', __name__)


@mod.route('/')
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)


@mod.route('/newmarker', methods=['post'])
def newmarker():
    try:
        print(request.form)
        return jsonify({'message': 'ok'})
    except Exception, e:
        return jsonify({'message': 'error', 'value': str(e)})
