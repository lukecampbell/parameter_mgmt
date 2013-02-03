#!/usr/bin/env python
'''
@author Luke Campbell <LCampbell at ASAScience dot com>
@file pmgmt/app.py
'''

from gevent.monkey import patch_all
patch_all()

from flask import Flask, render_template, url_for, redirect
from controllers.parameters import parameters


port = 5201

app = Flask('monitor', template_folder='pmgmt/templates', static_folder='pmgmt/static')

@app.route('/')
def index():
    return render_template('index.html')


app.add_url_rule('/parameters','parameters',parameters)



if __name__ == '__main__':
    app.run(debug=True, port=port)


