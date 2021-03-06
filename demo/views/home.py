# -*- coding: utf-8 -*-
from jinja2 import TemplateNotFound
from flask import Blueprint, render_template, abort, request, jsonify
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
    except Exception as e:
        return jsonify({'message': 'error', 'value': str(e)})
