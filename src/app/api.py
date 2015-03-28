from flask import Flask
from flask import request
from flask import g

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

#    "geo": "location",
#    "cip2011_4": "field_of_study",
#    "age": "age",
#    "noc2011": "occupation",
#    "hcdd_14v": "education_level"


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


def build_ranking_query(d):
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


@app.route("/api/v1/ranking")
def employment_ranking():
    pass
    # all you need is e.g.
    # select noc2011, observation_value from data where cip2011_4=7 and occupation_cat3 is not null order by noc2011 limit 10;


@app.route('/api/v1/ratios')
def ratios():
    pass
    # get query params
    # query db
    # get totals
    # get denominators
    # build json
    # return


# occupation categories
# field of study categories
# location
# age

# value
# totals
# ratios


# given a field of study
    # return the top 10 industries by total, ratio

# denominators can be found by walking up the category tree.

# note that you have to limit some variables:

# code2015=# SELECT SUM(observation_value) FROM data WHERE GEO=1 AND NOC2011=1 AND CIP2011_4=1 AND AGE=1 AND (HCDD_14V=2 OR HCDD_14V=3 OR HCDD_14V=4);


if __name__ == '__main__':
    app.debug = True
    app.run()
