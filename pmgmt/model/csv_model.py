import csv
import sqlite3


parameter_schema = '''CREATE TABLE parameters(
    id INTEGER PRIMARY KEY,
    name VARCHAR(32),
    hid VARCHAR(64),
    parameter_type VARCHAR(32),
    value_encoding VARCHAR(32),
    code_set VARCHAR(32),
    uom VARCHAR(32),
    fill_value VARCHAR(32),
    display_name VARCHAR(64),
    standard_name VARCHAR(32),
    long_name VARCHAR(32),
    data_product VARCHAR(32),
    url_refs VARCHAR(64))'''

parameter_dict_schema = '''CREATE TABLE pdict(
    id INTEGER PRIMARY KEY,
    name VARCHAR(32),
    description VARCHAR(128))'''

pdict_param_schema = '''CREATE TABLE pdict_param(
    pdict_id INTEGER NOT NULL,
    param_id INTEGER NOT NULL,
    PRIMARY KEY (pdict_id,param_id))'''

cursor = None


def initialize_models(cursor_path=None):
    db = sqlite3.connect(cursor_path or ':memory:')
    global cursor
    cursor = db.cursor()
    cursor.execute(parameter_schema)
    cursor.execute(parameter_dict_schema)
    cursor.execute(pdict_param_schema)
    with open('pmgmt/model/ParameterDefs.csv', 'r') as f:
        dr = csv.DictReader(f)
        for row in dr:
            if 'doc' in row['Scenario'].lower():
                continue
            if row['SKIP']:
                continue
            try:
                sql_cmd = 'INSERT INTO parameters VALUES (%s,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");' % (row['ID'][2:], row['Name'], row['HID'], row['Parameter Type'], row['Value Encoding'], row['Code Set'], row['Unit of Measure'], row['Fill Value'], row['Display Name'], row['Standard Name'], row['Long Name'], row['Data Product Identifier'], row['Reference URLS'])
                print sql_cmd
                cursor.execute(sql_cmd)
            except Exception as e:
                print row
                print e.message
                raise
    with open('pmgmt/model/ParameterDictionary.csv','r') as f:
        dr = csv.DictReader(f)
        for row in dr:
            if 'doc' in row['Scenario'].lower():
                continue
            if row['SKIP']:
                continue
            try:
                sql_cmd = 'INSERT INTO pdict VALUES(%s,"%s","%s")' % (row['ID'][4:], row['name'], row['parameters'])
                print sql_cmd
                cursor.execute(sql_cmd)
            except Exception as e:
                print row
                print e.message
                raise

            pd_ids = row['parameter_ids'].replace(' ','').replace('\n', '').split(',')
            for pd_id in pd_ids:
                try:
                    sql_cmd = 'INSERT INTO pdict_param VALUES(%s,%s)' % (row['ID'][4:], pd_id[2:])
                    print sql_cmd
                    cursor.execute(sql_cmd)
                except Exception as e:
                    print row
                    print e.message
                    raise
    db.commit()
    return cursor


