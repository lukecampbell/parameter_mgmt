
from flask import render_template, g
from pmgmt.model.model import Parameter

def parameters():
    connection = g.connection
    parameters = Parameter.list(connection)
    return render_template('parameters.html', parameters=parameters)

def parameter(pid='0'):
    connection = g.connection
    parameters = Parameter.where(connection, 'id=%s' % pid)
    return render_template('parameter.html', parameter=parameters[0])

