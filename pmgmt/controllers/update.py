
from flask import render_template, redirect, url_for, g

from pmgmt.model.model import initialize_parameters, initialize_parameter_dictionaries, read_parameters, read_parameter_dictionaries
from pmgmt.model.download_model import get, categories

def update():
    connection = g.connection
    for k in categories.iterkeys():
        get(k)
    connection.cursor.execute('DROP TABLE Parameter')
    connection.cursor.execute('DROP TABLE ParameterDictionary')
    initialize_parameters(connection)
    initialize_parameter_dictionaries(connection)
    read_parameters(connection)
    read_parameter_dictionaries(connection)
    return redirect(url_for('parameters'))




