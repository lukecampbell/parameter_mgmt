#!/usr/bin/env python
'''
@author Luke Campbell <LCampbell at ASAScience dot com>
@file pmgmt/app.py
'''

try:
    from gevent.monkey import patch_all
    patch_all()
except ImportError:
    # If we're using gevent, monkey patch everything before the app launches.
    pass

from model.csv_model import initialize_models
initialize_models()

from flask import Flask, render_template, url_for, redirect
from controllers.parameters import parameters, parameter
from controllers.parameter_dictionary import parameter_dictionaries, parameter_dictionary
from controllers.update import update

port = 5201

app = Flask('monitor', template_folder='pmgmt/templates', static_folder='pmgmt/static')

@app.route('/')
def index():
    return redirect(url_for('parameters'))


app.add_url_rule('/update','update',update)
app.add_url_rule('/parameters','parameters',parameters)
app.add_url_rule('/parameter/<pid>','parameter',parameter)
app.add_url_rule('/pdicts','parameter_dictionaries',parameter_dictionaries)
app.add_url_rule('/pdict/<pdict_id>','parameter_dictionary',parameter_dictionary)


if __name__ == '__main__':
    app.run(debug=True, port=port)


