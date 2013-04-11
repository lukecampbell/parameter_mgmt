
from flask import render_template, redirect, url_for

from model.csv_model import initialize_models
from model.download_model import get, categories

def update():
    for k in categories.iterkeys():
        get(k)
    initialize_models()
    return redirect(url_for('parameters'))




