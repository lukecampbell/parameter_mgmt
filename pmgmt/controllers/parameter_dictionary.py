
from flask import render_template
from model.csv_model import cursor


def parameter_dictionaries():
    cursor.execute('SELECT name,description FROM pdict')
    pdicts = {row[0] : row for row in cursor.fetchall()}

    return render_template('pdicts.html', pdicts=pdicts)

