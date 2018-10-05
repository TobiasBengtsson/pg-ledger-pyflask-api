from datetime import datetime
from flask import jsonify, request, url_for
from . import main
from app import db

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
