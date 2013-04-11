
from flask import render_template
from model.csv_model import get_cursor
from model.parameter_dictionary import ParameterDictionary
from model.parameter import Parameter


def parameter_dictionaries():
    cursor = get_cursor()
    cursor.execute('SELECT * FROM pdict')
    pdicts = [ParameterDictionary(*row) for row in cursor.fetchall()]
    for pdict in pdicts:
        cursor.execute('SELECT * FROM parameters WHERE id==?', (pdict.temporal_id,))
        parameters = [Parameter(*row) for row in cursor.fetchall()]
        pdict.temporal_id = parameters[0]
        cursor.execute('SELECT parameters.* FROM parameters INNER JOIN pdict_param ON parameters.id=pdict_param.param_id WHERE pdict_param.pdict_id==?', (pdict._id,))
        parameters = [Parameter(*row) for row in cursor.fetchall()]
        pdict.parameters = parameters

    return render_template('pdicts.html', pdicts=pdicts)

def parameter_dictionary(pdict_id='1'):
    cursor = get_cursor()
    cursor.execute('SELECT * FROM pdict WHERE id==?', (pdict_id,))
    pdicts = [ParameterDictionary(*row) for row in cursor.fetchall()]
    for pdict in pdicts:
        cursor.execute('SELECT * FROM parameters WHERE id==?', (pdict.temporal_id,))
        parameters = [Parameter(*row) for row in cursor.fetchall()]
        pdict.temporal_id = parameters[0]
        cursor.execute('SELECT parameters.* FROM parameters INNER JOIN pdict_param ON parameters.id=pdict_param.param_id WHERE pdict_param.pdict_id==?', (pdict._id,))
        parameters = [Parameter(*row) for row in cursor.fetchall()]
        pdict.parameters = parameters
    return render_template('pdict.html', pdict=pdicts[0])

