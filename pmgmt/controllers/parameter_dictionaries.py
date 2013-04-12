
from flask import render_template, g
from pmgmt.model.model import ParameterDictionary, Parameter
from types import MethodType


def parameter_dictionaries():
    connection = g.connection
    parameter_dictionaries = ParameterDictionary.list(connection)

    return render_template('pdicts.html', pdicts=parameter_dictionaries)

def parameter_dictionary(pdict_id='1'):
    connection = g.connection
    parameter_dictionaries = ParameterDictionary.where(connection,'id=%s' % pdict_id)
    for pdict in parameter_dictionaries:
        pdict.parameters = [Parameter.where(connection,'id=%s'%i)[0] for i in pdict.parameters]
        pdict.list_parameter_links = MethodType(list_parameter_links, pdict, ParameterDictionary)
    return render_template('pdict.html', pdict=parameter_dictionaries[0])


def list_parameter_links(self):
    parameter_links = ["<a href='/parameter/%s'>%s</a>" % (p._id, p.name) for p in self.parameters]
    return ', '.join(parameter_links)
