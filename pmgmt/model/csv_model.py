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

cursor = None


def initialize_models():
    db = sqlite3.connect(':memory:')
    global cursor
    cursor = db.cursor()
    cursor.execute(parameter_schema)
    with open('pmgmt/model/Parameters.csv', 'r') as f:
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
                return

    return cursor

initialize_models()

