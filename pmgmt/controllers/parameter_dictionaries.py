
from flask import render_template, g
from pmgmt.model.model import ParameterDictionary, Parameter
from types import MethodType


def parameter_dictionaries():
    connection = g.connection
    parameter_dictionaries = ParameterDictionary.list(connection)
    if 'parameters' not in ParameterDictionary._fields:
        ParameterDictionary._fields.append('parameters')
    for pdict in parameter_dictionaries:
        parameters = connection.query_db('SELECT Parameter.* FROM Parameter INNER JOIN ParameterRelation ON Parameter.id=ParameterRelation.parameter_id WHERE ParameterRelation.parameter_dictionary_id=?', [pdict.id])
        parameters = [Parameter(**i) for i in parameters]
        pdict.parameters = parameters
        pdict.list_parameter_links = MethodType(list_parameter_links, pdict, ParameterDictionary)
        pdict.temporal_id = Parameter.where(connection, 'id=%s' % pdict.temporal_id or 7)[0]

    return render_template('pdicts.html', pdicts=parameter_dictionaries)

def parameter_dictionary(pdict_id='1'):
    connection = g.connection
    parameter_dictionaries = ParameterDictionary.where(connection,'id=%s' % pdict_id)
    if 'parameters' not in ParameterDictionary._fields:
        ParameterDictionary._fields.append('parameters')
    for pdict in parameter_dictionaries:
        parameters = connection.query_db('SELECT Parameter.* FROM Parameter INNER JOIN ParameterRelation ON Parameter.id=ParameterRelation.parameter_id WHERE ParameterRelation.parameter_dictionary_id=?', [pdict.id])
        parameters = [Parameter(**i) for i in parameters]
        pdict.parameters = parameters
        pdict._fields.append('parameters')
        pdict.list_parameter_links = MethodType(list_parameter_links, pdict, ParameterDictionary)
        pdict.temporal_id = Parameter.where(connection, 'id=%s' % pdict.temporal_id or 7)[0]
    return render_template('pdict.html', pdict=parameter_dictionaries[0])


def list_parameter_links(self):
    parameter_links = ["<a href='/parameter/%s'>%s</a>" % (p.id, p.name) for p in self.parameters]
    return ', '.join(parameter_links)
