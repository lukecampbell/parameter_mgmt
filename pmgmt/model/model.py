

from flask_mvc.model.sqlite import Connection, parse_model, ObjectFactory
import pkg_resources
import csv
import pmgmt

Parameter = ObjectFactory.create_from_yaml('Parameter', pkg_resources.resource_filename(pmgmt.__name__,'resources/Parameter.yml'))
ParameterDictionary = ObjectFactory.create_from_yaml('ParameterDictionary', pkg_resources.resource_filename(pmgmt.__name__, 'resources/ParameterDictionary.yml'))

ParameterRelation = ObjectFactory.create_from_yaml('ParameterRelation', pkg_resources.resource_filename(pmgmt.__name__, 'resources/ParameterRelation.yml'))


filters = {
        '\xc2\xb0' : 'deg',
        '\xc3\x82' : '',
        '\xc2\xb5' : 'u',
        '\xce\xbc' : 'u',
        '\xc3\x8e\xc2\xbc' : 'u',
        '\xe2\x80\x9c':'"',
        '\xe2\x80\x9d':'"',
        }

def unicode_filter(input_dict):
    for key,value in input_dict.iteritems():
        if '"' in value:
            input_dict[key] = value.replace('"','')
        if not all(map(lambda x: ord(x) < 128,value)):
            for k,v in filters.iteritems():
                if k in value:
                    print 'Replacing ', k, ' with ', v
                    input_dict[key] = value.replace(k,v)
                    value = value.replace(k,v)
                    print value
            if not all(map(lambda x:ord(x)<128,value)):
                for s in value:
                    if ord(s) >= 128:
                        print 'Unrecognized character'
                        print ord(s)
                        print s
                print 'Unable to fix string'
                print value
                print input_dict['ID']


def initialize_parameter_relations(connection):
    connection.conn.text_factory = str
    ParameterRelation.initialize(connection)

def initialize_parameter_dictionaries(connection):
    connection.conn.text_factory = str
    ParameterDictionary.initialize(connection)

def read_parameter_dictionaries(connection, path=''):
    connection.conn.text_factory = str
    path = path or pkg_resources.resource_filename(pmgmt.__name__,'resources/ParameterDictionary.csv')
    with open(path,'r') as f:
        dr = csv.DictReader(f)
        for row in dr:
            if 'doc' in row['Scenario'].lower():
                continue
            if row['SKIP']:
                continue
            if 'void' in row['Scenario'].lower():
                continue
            unicode_filter(row)
            parameter_dictionary = ParameterDictionary(
                    id=row['ID'][4:],
                    name=row['name'],
                    temporal_id=row['temporal_parameter'][2:]
                    )
            parameter_dictionary.create(connection)
            for pid in row['parameter_ids']:
                pass

        connection.commit()



def initialize_parameters(connection):
    connection.conn.text_factory = str
    Parameter.initialize(connection)

def read_parameters(connection, path=''):
    connection.conn.text_factory = str
    path = path or pkg_resources.resource_filename(pmgmt.__name__,'resources/ParameterDefs.csv')
    with open(path,'r') as f:
        dr = csv.DictReader(f)
        for row in dr:
            if 'doc' in row['Scenario'].lower():
                continue
            if row['SKIP']:
                continue
            if 'void' in row['Scenario'].lower():
                continue

            unicode_filter(row)

            parameter = Parameter(
                    id=row['ID'][2:], 
                    name=row['Name'],
                    parameter_type=row['Parameter Type'],
                    value_encoding=row['Value Encoding'],
                    code_set=row['Code Set'],
                    uom=row['Unit of Measure'],
                    precision=row['Precision'],
                    fill_value=row['Fill Value'],
                    display_name=row['Display Name'],
                    standard_name=row['Standard Name'],
                    long_name=row['Long Name'],
                    data_product=row['Data Product Identifier']
                    )
            parameter.create(connection)
    connection.commit()




