"""The api.

Usage:
    api.py <category_mapping_file>

Arguments:
    <category_mapping_file>  The path to the category mapping file. 
"""

from flask import Flask
from flask import request
from flask import g

from docopt import docopt

import json
import psycopg2
import copy

from src.db import get_cursor

app = Flask(__name__)

DEFAULTS = {
    "geo": [1],
    "cip2011_4": [1],
    "age": [1],
    "noc2011": [1],
    "hcdd_14v": [4]
}

# this should be in its own database table
CATEGORY_MAPPING = None


@app.before_request
def before_request():
    g.cur = get_cursor() 
    g.d = copy.copy(DEFAULTS)
    for k in g.d:
        v = request.args.get(k, None)
        if v:
            g.d[k] = v.split(",")
   
 
@app.teardown_request
def teardown_request(exception):
    cur = getattr(g, 'cur', None)
    if cur is not None:
        cur.close()


@app.route('/api/v1/status')
def status():
    return 'Hello World!'


def build_totals_query(d):
    q = "SELECT SUM(observation_value) FROM data WHERE "
    q += "AND ".join(
        [k + " IN (" + ",".join([str(j) for j in d[k]]) + ") " for k in d]
    )
    q += ";"
    return q


@app.route('/api/v1/total')
def total(): 
    q = build_totals_query(g.d) 
    g.cur.execute(q)

    if g.cur.rowcount > 1:
        raise ValueError("found more than one value for query")
    elif g.cur.rowcount == 0:
        raise ValueError("found no data for query")
    
    return str(g.cur.fetchone()[0])


def build_rank_query(d):
    q = "select noc2011, observation_value from data where "
    q += "and ".join(
        [k + " in (" + ",".join([str(j) for j in d[k]]) + ") " 
        for k in d if k != "noc2011"]
    )
    q += (" and observation_value is not null "
         " and occupation_cat3 is not null "
         " order by observation_value desc "
         " limit 10;")
    return q


@app.route("/api/v1/rank")
def rank():
    q = build_rank_query(g.d)    
    g.cur.execute(q)
    
    result = {"rank": []}
    for r in g.cur.fetchall():
        n = CATEGORY_MAPPING["NOC2011"][str(r[0])]
        result["rank"].append({
            "name": n["category_name"], 
            "count": r[1]
        })
    return str(result)


if __name__ == '__main__':
    args = docopt(__doc__)
    
    CATEGORY_MAPPING = json.loads(
        "".join(open(args["<category_mapping_file>"], "r"))
    )
    
    app.debug = True
    app.run()
    
