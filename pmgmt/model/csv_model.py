import csv
import sqlite3

cursor = None

parameter_schema = '''CREATE TABLE parameters(
    id INTEGER PRIMARY KEY,
    name VARCHAR(32),
    parameter_type VARCHAR(32),
    value_encoding VARCHAR(32),
    code_set VARCHAR(32),
    uom VARCHAR(32),
    fill_value VARCHAR(32),
    display_name VARCHAR(64),
    standard_name VARCHAR(32),
    long_name VARCHAR(32),
    data_product VARCHAR(32))'''

parameter_dict_schema = '''CREATE TABLE pdict(
    id INTEGER PRIMARY KEY,
    name VARCHAR(32),
    teporal_id INTEGER NOT NULL)'''

pdict_param_schema = '''CREATE TABLE pdict_param(
    pdict_id INTEGER NOT NULL,
    param_id INTEGER NOT NULL,
    PRIMARY KEY (pdict_id,param_id))'''

def get_cursor():
    global cursor
    return cursor


filters = {
        '\xc2\xb0' : 'deg',
        '\xc3\x82' : '',
        '\xc2\xb5' : 'u',
        '\xce\xbc' : 'u',
        '\xc3\x8e\xc2\xbc' : 'u',
        '\xe2\x80\x9c':'"',
        '\xe2\x80\x9d':'"',
        }

def initialize_models(cursor_path=None):
    db = sqlite3.connect(cursor_path or ':memory:')
    db.text_factory = str
    global cursor
    cursor = db.cursor()
    cursor.execute(parameter_schema)
    cursor.execute(parameter_dict_schema)
    cursor.execute(pdict_param_schema)
    with open('pmgmt/model/ParameterDefs.csv', 'r') as f:
        dr = csv.DictReader(f)
        for row in dr:
            for key,value in row.iteritems():
                if '"' in value:
                    row[key] = value.replace('"','')
                if not all(map(lambda x: ord(x) < 128,value)):
                    for k,v in filters.iteritems():
                        if k in value:
                            print 'Replacing ', k, ' with ', v
                            row[key] = value.replace(k,v)
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
                        print row['ID']


            if 'doc' in row['Scenario'].lower():
                continue
            if row['SKIP']:
                continue
            if 'void' in row['Scenario'].lower():
                continue
            try:
                sql_cmd = 'INSERT INTO parameters VALUES (%s,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");' % (row['ID'][2:], row['Name'], row['Parameter Type'], row['Value Encoding'], row['Code Set'], row['Unit of Measure'], row['Fill Value'], row['Display Name'], row['Standard Name'], row['Long Name'], row['Data Product Identifier'])
                cursor.execute(sql_cmd)
            except Exception as e:
                raise
    with open('pmgmt/model/ParameterDictionary.csv','r') as f:
        dr = csv.DictReader(f)
        for row in dr:
            if 'doc' in row['Scenario'].lower():
                continue
            if row['SKIP']:
                continue
            try:
                if not row['temporal_parameter']:
                    row['temporal_parameter'] = 'PD7'
                sql_cmd = 'INSERT INTO pdict VALUES(%s,"%s","%s")' % (row['ID'][4:], row['name'], row['temporal_parameter'][2:])
                cursor.execute(sql_cmd)
            except Exception as e:
                raise

            pd_ids = row['parameter_ids'].replace(' ','').replace('\n', '').split(',')
            for pd_id in pd_ids:
                try:
                    sql_cmd = 'INSERT INTO pdict_param VALUES(%s,%s)' % (row['ID'][4:], pd_id[2:])
                    cursor.execute(sql_cmd)
                except Exception as e:
                    raise
    db.commit()
    return cursor


