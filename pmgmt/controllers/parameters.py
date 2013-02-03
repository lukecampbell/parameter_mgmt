
from flask import render_template
from model.csv_model import cursor


def parameters():
    cursor.execute('SELECT name FROM parameters')
    names = [row[0] for row in cursor.fetchall()]
    return render_template('parameters.html', names=names)
