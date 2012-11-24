#!/usr/bin/env python

import MySQLdb
import tpconf


def check_and_create_db():
    db_name = tpconf.FREQUENCY_STORE['db']
    e_query = '''
        SELECT EXISTS(
        SELECT 1
        FROM information_schema.schemata
        WHERE schema_name = '{}'
        ) AS e
        '''.format(db_name)
    rs = cursor.execute(e_query)
    exists = cursor.fetchone()[0]
    if not exists:
        cursor.execute('''
            CREATE DATABASE {}
            '''.format(db_name))
        server.commit()


def check_and_create_table():
    db_name = tpconf.FREQUENCY_STORE['db']
    table_name = tpconf.FREQUENCY_STORE['table']['name']
    table_def = tpconf.FREQUENCY_STORE['table']['def']
    e_query = '''
        SELECT EXISTS(
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = '{}'
            AND table_name = '{}'
        ) AS e
        '''.format(db_name, table_name)
    rs = cursor.execute(e_query)
    exists = cursor.fetchone()[0]
    if not exists:
        cursor.execute('''
            CREATE TABLE {}.{} {}
            '''.format(db_name, table_name, table_def))
        server.commit()


if __name__ == '__main__':

    server = MySQLdb.connect(**tpconf.FREQUENCY_STORE['connpar'])
    cursor = server.cursor()
    
    check_and_create_db()
    check_and_create_table()

    
