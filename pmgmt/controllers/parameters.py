
from flask import render_template
from model.csv_model import get_cursor
from model.parameter import Parameter


def parameters():
    cursor = get_cursor()
    cursor.execute('SELECT * FROM parameters')
    parameters = [Parameter(*row) for row in cursor.fetchall()]
    return render_template('parameters.html', parameters=parameters)

def parameter(pid='0'):
    cursor = get_cursor()
    cursor.execute('SELECT * FROM parameters WHERE ID=?', (pid,))
    parameters = [Parameter(*row) for row in cursor.fetchall()]
    return render_template('parameter.html', parameter=parameters[0])

