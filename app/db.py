import psycopg2
from flask import current_app, g

def get_db():
    if 'db_conn' not in g:
        g.db_conn = psycopg2.connect(current_app.config['PG_LEDGER_CONNECTION_STRING'])

    return g.db_conn

def close_db(e=None):
    db_conn = g.pop('db_conn', None)

    if db_conn is not None:
        db_conn.close()

def init_app(app):
    app.teardown_appcontext(close_db)
