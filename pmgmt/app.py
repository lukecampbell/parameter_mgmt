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



from flask import Flask, render_template, url_for, redirect, g
from flask_mvc.model.sqlite import Connection
from pmgmt.controllers.parameters import parameters, parameter
from pmgmt.controllers.parameter_dictionaries import parameter_dictionaries, parameter_dictionary
from pmgmt.controllers.update import update
from pmgmt.util.config import read_config

config = read_config()
connection = Connection(config['database'])
if config['database']==':memory:':
    from pmgmt.model.model import initialize_parameters, initialize_parameter_dictionaries, read_parameters, read_parameter_dictionaries
    initialize_parameters(connection)
    initialize_parameter_dictionaries(connection)
    read_parameters(connection)
    read_parameter_dictionaries(connection)

app = Flask('monitor', template_folder=config['template_folder'], static_folder=config['static_folder'])


@app.before_request
def before_request():
    g.connection = connection

@app.teardown_request
def teardown_request(exception):
    g.connection.commit()

@app.route('/')
def index():
    return redirect(url_for('parameters'))


app.add_url_rule('/update','update',update)
app.add_url_rule('/parameters','parameters',parameters)
app.add_url_rule('/parameter/<pid>','parameter',parameter)
app.add_url_rule('/pdicts','parameter_dictionaries',parameter_dictionaries)
app.add_url_rule('/pdict/<pdict_id>','parameter_dictionary',parameter_dictionary)


def main():
    app.run(debug=config['debug'], port=config['port'])



if __name__ == '__main__':
    main()


