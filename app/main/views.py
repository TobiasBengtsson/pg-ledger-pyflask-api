from datetime import datetime
from flask import jsonify, request, url_for
from . import main
from app import db

def trim_account_name(account_full_name):
    components = account_full_name.split(':')
    trimmed_components = []
    for component in components:
        trimmed_components.append(component.strip())
    
    return ':'.join(trimmed_components)

@main.route('/accounts', methods=['GET'])
def getAccounts():
    skip = request.args.get('skip', type = int) or 0
    take = request.args.get('take', type = int) or 100
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT full_name
        FROM public.account
        ORDER BY full_name
        LIMIT %s
        OFFSET %s;
        """,
        (take, skip))
    all_rows = cur.fetchall()
    cur.execute('SELECT COUNT(*) FROM public.account')
    count = cur.fetchone()
    cur.close()
    return jsonify(
        totalCount = count[0],
        accounts = list(map(lambda x: { 'accountFullName': x[0] }, all_rows))), 200

@main.route('/accounts', methods=['POST'])
def addAccount():
    try:
        request_body = request.get_json()
        account_full_name = trim_account_name(request_body['accountFullName'])
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM public.account WHERE full_name = %s;', (account_full_name, ))
        count = cur.fetchone()
        if count[0] is not 0:
            return '', 409
        cur.execute('SELECT public.add_account(%s);', (account_full_name, ))
        account_full_name = cur.fetchone()
        conn.commit()
        cur.close()
        return '', 201, {'Location': '/accounts/' + account_full_name[0]}
    except KeyError:
        return '', 400

@main.route('/accounts/<account_full_name>', methods=['GET'])
def getAccount(account_full_name):
    conn = db.get_db()
    cur = conn.cursor()
    account_full_name = trim_account_name(account_full_name)
    cur.execute('SELECT COUNT(*) FROM public.account WHERE full_name = %s;', (account_full_name, ))
    count = cur.fetchone()
    if count[0] is 0:
        return '', 404
    cur.close()
    return jsonify(accountFullName=account_full_name), 200
